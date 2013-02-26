from django import forms
from django.conf import settings

from paypal.standard import forms as paypal_form, widgets as paypal_widgets

class BuyNowForm(paypal_form.PayPalEncryptedPaymentsForm):
    undefined_quantity = forms.CharField(widget=paypal_widgets.ValueHiddenInput(), initial='1')
    weight = forms.CharField(widget=paypal_widgets.ValueHiddenInput())
    weight_unit = forms.CharField(widget=paypal_widgets.ValueHiddenInput(), initial='kgs')
    currency_code = forms.CharField(widget=forms.HiddenInput(), initial='EUR')
    no_shipping = forms.ChoiceField(widget=forms.HiddenInput(), initial='2')

    image_url = forms.ChoiceField(widget=paypal_widgets.ValueHiddenInput())

    def render(self):
        if getattr(settings, 'PAYPAL_TEST', True):
            return super(BuyNowForm, self).sandbox()
        else:
            return super(BuyNowForm, self).render()
