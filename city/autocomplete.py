from dal import autocomplete
from city.models import City
from warehouse.models import Warehouse


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()

        if self.q:
            qs = qs.filter(city_title__istartswith=self.q)
        return qs


class WarehouseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Warehouse.objects.all()

        if self.q:
            qs = qs.filter(address__icontains=self.q) | qs.filter(title__icontains=self.q)
        return qs


