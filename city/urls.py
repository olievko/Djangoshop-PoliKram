from django.urls import path
from .views import autocomplete, refresh
from .autocomplete import CityAutocomplete, WarehouseAutocomplete


urlpatterns = [
    # CITIES DATA BASE REFRESH
    path('refresh', refresh, name='refresh'),
    path('autocomplete', autocomplete, name='autocomplete'),
    # AUTOCOMPLETE CITIES + WAREHOUSES
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete'),
    path('warehouse-autocomplete/', WarehouseAutocomplete.as_view(), name='warehouse-autocomplete'),
]
