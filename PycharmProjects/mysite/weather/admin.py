from django.contrib import admin

from .models import CityWeather, HistoryReq

admin.site.register(CityWeather)
admin.site.register(HistoryReq)
