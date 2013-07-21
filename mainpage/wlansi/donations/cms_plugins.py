import decimal

from django import dispatch
from django.conf import settings
from django.contrib.sites import models as sites_models
from django.core import mail, urlresolvers
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import loader
from django.utils import timezone, translation
from django.utils.translation import pgettext_lazy, ugettext_lazy as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

import reversion

from ..buynow import signals as buynow_signals

from . import forms, models

class DonationsPlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays a list of donations.
    """

    module = 'wlan slovenija'
    name = _("Donations")
    render_template = 'donations/list.html'

    def render(self, context, instance, placeholder):
        context.update({
            'donations': models.Donation.objects.all(),
        })
        return context

plugin_pool.register_plugin(DonationsPlugin)

class SupportersPlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays a list of donations.
    """

    module = 'wlan slovenija'
    name = _("Supporters")
    render_template = 'donations/supporters.html'

    def render(self, context, instance, placeholder):
        context.update({
            'supporters': models.Donation.objects.exclude(donor=None).exclude(donor='').order_by('donor'),
        })
        return context

plugin_pool.register_plugin(SupportersPlugin)

def button_form(request, instance, cancel_return=None):
    if not cancel_return:
        cancel_return = request.build_absolute_uri()

    form = forms.DonateForm(initial={
        'business': settings.PAYPAL_RECEIVER_EMAIL_DONATION_ALIAS,
        'item_number': instance.donation_id,
        'item_name': instance.organization_name_or_service,
        'no_note': '0',
        'cn': _("Public message"),
        'cancel_return': cancel_return,
        'notify_url': request.build_absolute_uri(urlresolvers.reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(urlresolvers.reverse('paypal-donation')),
        'image_url': request.build_absolute_uri(staticfiles_storage.url('wlansi/images/paypal-logo.png')),
    })

    return form

class DonatePlugin(plugin_base.CMSPluginBase):
    """
    This plugin displays a button to donate through PayPal.
    """

    module = 'wlan slovenija'
    model = models.Donate
    name = pgettext_lazy(u'admin', u"Donate")
    render_template = "donations/button.html"
    text_enabled = True

    def render(self, context, instance, placeholder):
        request = context['request']
        form = button_form(request, instance)

        context.update({
            'paypal_test': getattr(settings, 'PAYPAL_TEST', True),
            'form': form,
            'object': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(DonatePlugin)

@dispatch.receiver(buynow_signals.transaction_new)
@reversion.create_revision()
def new_donation(sender, is_pdt, **kwargs):
    try:
        int(sender.item_number)
        # Item number is a number, thus not a donation ID (probably object ID)
        return
    except ValueError:
        pass

    timestamp = timezone.now()
    amount = decimal.Decimal(sender.mc_gross) - decimal.Decimal(sender.mc_fee) # Formula in donations/pdf.html as well
    donation_by = ' '.join((sender.first_name, sender.last_name))

    defaults = {
        'date': timestamp,
        'amount': amount,
        'donor': donation_by, # TODO: Support also anonymous donations (in that case this field should be blank)
        'message': sender.memo,
        'timestamp': timestamp,
        'donation_by': donation_by, # This field is internal and should still be filled for anonymous donations
        'email': sender.payer_email,
        'gross': sender.mc_gross,
        'fee': sender.mc_fee,
    }

    if is_pdt:
        defaults['pdt_id'] = sender.pk
    else:
        defaults['ipn_id'] = sender.pk

    donation, created = models.Donation.objects.get_or_create(txn_id=sender.txn_id, defaults=defaults)

    if not created:
        if is_pdt:
            reversion.set_comment("Got PDT, setting ID.")
            donation.pdt_id = sender.pk
        else:
            reversion.set_comment("Got IPN, setting ID.")
            donation.ipn_id = sender.pk

        if sender.test_ipn:
            reversion.set_comment("Got a test IPN, marking it as a test.")
            if donation.internal_comment:
                donation.internal_comment += ' Test.'
            else:
                donation.internal_comment += 'Test.'

        donation.save()

        # Donation has already been created
        return
    else:
        reversion.set_comment("Initial version.")

    site = sites_models.Site.objects.get_current()
    protocol = 'https' if getattr(settings, 'USE_HTTPS', False) else 'http'
    base_url = "%s://%s" % (protocol, site.domain)

    donation_url = urlresolvers.reverse(
        'admin:%s_%s_change' % (donation._meta.app_label, donation._meta.object_name.lower()), args=(donation.pk,)
    )
    donation_url = '%s%s' % (base_url, donation_url)

    # TODO: Should we reverse something here?
    home_url = '%s%s' % (base_url, '/')

    class Request(object):
        REQUEST = {
            'language': translation.get_language(),
        }
        current_page = None

    context = {
        'EMAIL_SUBJECT_PREFIX': settings.EMAIL_SUBJECT_PREFIX,
        'site': site,
        'protocol': protocol,
        'base_url': base_url,
        'home_url': home_url,
        'donation_url': donation_url,
        'obj': sender,
        'donation_by': donation_by,
        'amount': amount,
        'request': Request(), # Fake request object for page_url to work in e-mails
    }

    subject = loader.render_to_string('donations/new_donation_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string('donations/new_donation_email.txt', context)

    mail.send_mail(subject, email, None, [settings.PAYPAL_RECEIVER_EMAIL_DONATION_ALIAS])

    subject = loader.render_to_string('donations/donation_confirmation_subject.txt', context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    email = loader.render_to_string('donations/donation_confirmation_email.txt', context)

    mail.send_mail(subject, email, settings.PAYPAL_RECEIVER_EMAIL_DONATION_ALIAS, [sender.payer_email])
