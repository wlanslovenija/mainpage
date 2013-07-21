from django import forms
from django.conf import settings

from paypal.standard import forms as paypal_form, widgets as paypal_widgets

class BuyNowForm(paypal_form.PayPalEncryptedPaymentsForm):
    no_shipping = forms.CharField(widget=forms.HiddenInput(), initial='2')
    # Uncomment if you want a user to choose quantity at PayPal checkout
    #undefined_quantity = forms.CharField(widget=paypal_widgets.ValueHiddenInput(), initial='1')
    currency_code = forms.CharField(widget=forms.HiddenInput(), initial='EUR')

    handling = forms.CharField(widget=paypal_widgets.ValueHiddenInput())
    shipping = forms.CharField(widget=paypal_widgets.ValueHiddenInput())
    shipping2 = forms.CharField(widget=paypal_widgets.ValueHiddenInput())

    image_url = forms.ChoiceField(widget=paypal_widgets.ValueHiddenInput())

    cn = forms.ChoiceField(widget=paypal_widgets.ValueHiddenInput())

    def render(self):
        if getattr(settings, 'PAYPAL_TEST', True):
            return super(BuyNowForm, self).sandbox()
        else:
            return super(BuyNowForm, self).render()
