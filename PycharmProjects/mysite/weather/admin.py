from django.contrib import admin

from .models import CityWeather, HistoryReq, City

admin.site.register(CityWeather)
admin.site.register(HistoryReq)
admin.site.register(City)