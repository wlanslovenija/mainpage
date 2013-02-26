from django.views.decorators import csrf

from paypal.standard.pdt import views as pdt_views
from paypal.standard.ipn import views as ipn_views

# django-paypal does not use this decorator, so we are doing it ourselves
ipn = csrf.csrf_exempt(ipn_views.ipn)
pdt = pdt_views.pdt
