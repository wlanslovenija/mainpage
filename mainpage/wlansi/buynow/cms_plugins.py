import decimal

from django import dispatch
from django.conf import settings
from django.contrib.sites import models as sites_models
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core import mail, urlresolvers
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from paypal.standard.ipn import signals as ipn_signals
from paypal.standard.pdt import signals as pdt_signals

import reversion

from . import forms, models

def shipping(instance):
    if instance.weight <= 2:
        return decimal.Decimal('4.47')
    elif instance.weight <= 5:
        return decimal.Decimal('5.34')
    elif instance.weight <= 10:
        return decimal.Decimal('7.85')
    elif instance.weight <= 15:
        return decimal.Decimal('8.26')
    elif instance.weight <= 20:
        return decimal.Decimal('9.51')
    elif instance.weight <= 25:
        return decimal.Decimal('11.20')
    elif instance.weight <= 30:
        return decimal.Decimal('13.27')
    else:
        raise ValueError("Invalid weight: %s" % instance.weight)

def paypal_static():
    return decimal.Decimal('0.25')

def paypal_variate(price):
    return decimal.Decimal('0.029') * price

class BuyNowPlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays a button to buy now through PayPal.
    """

    module = 'wlan slovenija'
    model = models.BuyNow
    name = _("Buy now")
    render_template = "buynow/button.html"

    def render(self, context, instance, placeholder):
        request = context['request']

        handling = decimal.Decimal('0.0') # TODO: You decide!
        shipping_one = shipping(instance)
        shipping1 = paypal_static() + paypal_variate(instance.price + shipping_one + handling) + shipping_one
        shipping2 = paypal_variate(instance.price + shipping_one) + shipping_one

        form = forms.BuyNowForm(initial={
            'item_number': instance.pk,
            'item_name': instance.item_name,
            'amount': instance.price,
            'quantity': '1',
            'handling': '%.2f' % handling,
            'shipping': '%.2f' % shipping1,
            'shipping2': '%.2f' % shipping2,
            'cancel_return': request.build_absolute_uri(),
            'notify_url': request.build_absolute_uri(urlresolvers.reverse('paypal-ipn')),
            'return_url': request.build_absolute_uri(urlresolvers.reverse('paypal-pdt')),
            'image_url': request.build_absolute_uri(staticfiles_storage.url('wlansi/images/paypal-logo.png')),
        })

        context.update({
            'paypal_test': getattr(settings, 'PAYPAL_TEST', True),
            'form': form,
            'object': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(BuyNowPlugin)

@reversion.create_revision()
def new_order(obj, is_pdt):
    order_by = ' '.join((obj.first_name, obj.last_name))

    shipping_address_tuple = (
        obj.address_name,
        obj.address_street,
        obj.address_city,
        ' '.join((obj.address_state, obj.address_zip)),
        obj.address_country,
    )

    defaults = {
        'item_id': obj.item_number,
        'quantity': obj.quantity,
        'order_by': order_by,
        'email': obj.payer_email,
        'phone': obj.contact_phone,
        'shipping_address': '\n'.join(shipping_address_tuple),
        'state': 'test' if obj.test_ipn else 'pending',
    }

    if is_pdt:
        defaults['pdt_id'] = obj.pk
    else:
        defaults['ipn_id'] = obj.pk

    order, created = models.Order.objects.get_or_create(txn_id=obj.txn_id, defaults=defaults)

    if not created:
        if is_pdt:
            reversion.set_comment("Got PDT, setting ID.")
            order.pdt_id = obj.pk
        else:
            reversion.set_comment("Got IPN, setting ID.")
            order.ipn_id = obj.pk

        if obj.test_ipn:
            reversion.set_comment("Got a test IPN, setting test state.")
            order.state = 'test'

        order.save()

        # Order has already been created
        return
    else:
        reversion.set_comment("Initial version.")

        shipping_one = shipping(order.item)
        item_and_shipping = decimal.Decimal('%.2f' % (order.item.price + shipping_one))
        order.handling = obj.mc_gross - obj.mc_fee - obj.quantity * item_and_shipping
        order.save()

    site = sites_models.Site.objects.get_current()
    protocol = 'https' if getattr(settings, 'USE_HTTPS', False) else 'http'
    base_url = "%s://%s" % (protocol, site.domain)

    order_url = urlresolvers.reverse(
        'admin:%s_%s_change' % (order._meta.app_label, order._meta.object_name.lower()), args=(order.pk,)
    )
    order_url = '%s%s' % (base_url, order_url)

    # TODO: Should we reverse something here?
    home_url = '%s%s' % (base_url, '/')

    context = {
        'EMAIL_SUBJECT_PREFIX': settings.EMAIL_SUBJECT_PREFIX,
        'site': site,
        'protocol': protocol,
        'base_url': base_url,
        'home_url': home_url,
        'order_url': order_url,
        'obj': obj,
        'ordered_by': order_by,
        'shipping_address': ', '.join(shipping_address_tuple),
    }

    subject = loader.render_to_string('buynow/new_order_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string('buynow/new_order_email.txt', context)

    mail.send_mail(subject, email, None, [settings.PAYPAL_RECEIVER_EMAIL])

    subject = loader.render_to_string('buynow/order_confirmation_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string('buynow/order_confirmation_email.txt', context)

    mail.send_mail(subject, email, settings.PAYPAL_RECEIVER_EMAIL, [obj.payer_email])

def error_order(obj, is_pdt=True):
    site = sites_models.Site.objects.get_current()
    protocol = 'https' if getattr(settings, 'USE_HTTPS', False) else 'http'
    base_url = "%s://%s" % (protocol, site.domain)

    obj_url = urlresolvers.reverse(
        'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.object_name.lower()), args=(obj.pk,)
    )
    obj_url = '%s%s' % (base_url, obj_url)

    # TODO: Should we reverse something here?
    home_url = '%s%s' % (base_url, '/')

    context = {
        'EMAIL_SUBJECT_PREFIX': settings.EMAIL_SUBJECT_PREFIX,
        'site': site,
        'protocol': protocol,
        'base_url': base_url,
        'home_url': home_url,
        'obj_url': obj_url,
        'obj': obj,
    }

    subject = loader.render_to_string('buynow/error_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string('buynow/error_email.txt', context)

    mail.send_mail(subject, email, None, [settings.PAYPAL_RECEIVER_EMAIL])

@dispatch.receiver(pdt_signals.pdt_successful)
def pdt_successful(sender, **kwargs):
    # Save initial revision
    with reversion.create_revision():
        reversion.set_comment("Initial version.")
        sender.save()

    if sender.flag_info:
        # django-paypal is buggy in handling invalid PDTs, so we check flag_info manually
        sender.flag = True
        with reversion.create_revision():
            reversion.set_comment("Flagging PDT.")
            sender.save()
        sender.send_signals()
        return

    new_order(sender, True)

@dispatch.receiver(pdt_signals.pdt_failed)
def pdt_failed(sender, **kwargs):
    error_order(sender, True)

@dispatch.receiver(ipn_signals.payment_was_successful)
def payment_was_successful(sender, **kwargs):
    # Save initial revision
    with reversion.create_revision():
        reversion.set_comment("Initial version.")
        sender.save()

    new_order(sender, False)

@dispatch.receiver(ipn_signals.payment_was_flagged)
def payment_was_flagged(sender, **kwargs):
    error_order(sender, False)
