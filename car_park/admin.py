from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import CarPark


class CarParkAdmin(OSMGeoAdmin):
    list_display = ("name", "location")


admin.site.register(CarPark, CarParkAdmin)
