import decimal

from django import http, shortcuts
from django.views.decorators import csrf, http as http_decorators
from django.utils.translation import ugettext_lazy as _

from paypal.standard.pdt import views as pdt_views
from paypal.standard.ipn import views as ipn_views

from . import cms_plugins, models

# django-paypal does not use this decorator, so we are doing it ourselves
ipn = csrf.csrf_exempt(ipn_views.ipn)
pdt = pdt_views.pdt

@http_decorators.require_POST
def paypal_button(request):
    instance = shortcuts.get_object_or_404(models.BuyNow, pk=request.POST['instance'])

    try:
        handling = decimal.Decimal(request.POST['handling'])
        if not handling.is_finite() or handling.is_signed():
            return http.HttpResponseBadRequest(_("Invalid value: %(handling)s") % {'handling': request.POST['handling']})
    except decimal.DecimalException:
        return http.HttpResponseBadRequest(_("Invalid value: %(handling)s") % {'handling': request.POST['handling']})

    # TODO: Can we just like this pass cancel_return parameter? Is this secure?
    form = cms_plugins.button_form(request, instance, handling, request.POST['cancel_return'])

    return http.HttpResponse(form.render())
