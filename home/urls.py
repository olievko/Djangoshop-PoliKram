from django.urls import path
from .views import aboutus, warranty, shipmentpayment, purchasereturn, contact

from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path(_('about/'), aboutus, name='aboutus'),
    path(_('warranty/'), warranty, name='warranty'),
    path(_('shipment/payment/'), shipmentpayment, name='shipmentpayment'),
    path(_('return/'), purchasereturn, name='purchasereturn'),
    path(_('contact/'), contact, name='contact'),
]