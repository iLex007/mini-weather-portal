from django.db import models
from django.utils import timezone
from datetime import datetime


class City(models.Model):
    city = models.CharField(max_length=20)

    def __str__(self):
        return self.city


class CityWeather(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateTimeField('date requested', default=timezone.now())
    temp = models.FloatField(default=0)
    description = models.CharField(max_length=200, default='')
    icon = models.CharField(max_length=10, default='')
    cod = models.IntegerField(default=0)

    def __str__(self):
        return self.city_name


class HistoryReq(models.Model):
    date_to = models.DateTimeField(default=timezone.now())
    date_from = models.DateTimeField(default=datetime(2020, 10, 17, 11, 24, 32))
    city = models.CharField(max_length=20, default="All")
