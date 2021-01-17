from django.contrib import admin
from city.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['city_title', 'region', 'area']
    search_fields = ['city_title']
