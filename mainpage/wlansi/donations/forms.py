from django import forms
from django.conf import settings
from django.utils import safestring
from django.utils.translation import ugettext_lazy as _

from paypal.standard import conf as paypal_conf, widgets as paypal_widgets

from ..buynow import forms as buynow_forms

class DonateForm(buynow_forms.BuyNowForm):
    cmd = forms.CharField(widget=forms.HiddenInput(), initial='_donations')

    no_shipping = forms.CharField(widget=forms.HiddenInput(), initial='1')
    undefined_quantity = forms.CharField(widget=paypal_widgets.ValueHiddenInput())

    def _render(self):
        return safestring.mark_safe(
            u"""<form action="%s" method="post">%s<input type="image" src="%s" border="0" name="submit" alt="Donate" title="%s" /></form>""" % (
                paypal_conf.POSTBACK_ENDPOINT, self.as_p(), self.get_image(), _("Donate with PayPal"),
            )
        )

    def sandbox(self):
        return safestring.mark_safe(
            u"""<form action="%s" method="post">%s<input type="image" src="%s" border="0" name="submit" alt="Donate" title="%s" /></form>""" % (
                paypal_conf.SANDBOX_POSTBACK_ENDPOINT, self.as_p(), self.get_image(), _("Donate with PayPal"),
            )
        )

    def get_image(self):
        if paypal_conf.TEST:
            return settings.PAYPAL_SANDBOX_DONATE_IMAGE
        else:
            return settings.PAYPAL_DONATE_IMAGE

    def render(self):
        if getattr(settings, 'PAYPAL_TEST', True):
            return self.sandbox()
        else:
            return self._render()
