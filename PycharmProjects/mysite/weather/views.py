from . models import CityWeather, HistoryReq
from django.shortcuts import render, redirect
import requests
from .forms import CityReqForm, HistoryReqForm, CityForm
from django.core.paginator import Paginator


def index(request):

    appid = '57bd238729c465144436fe7e688d6e2d'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == 'POST':
        form = CityReqForm(request.POST)
        if form.is_valid():
            form.save()

        if len(CityWeather.objects.all()) == 0:
            city = 'Vinica'
            res = requests.get(url.format(city)).json()

        else:
            try:
                city_weather = CityWeather.objects.order_by('-id')[0]
                city = city_weather.city_name
                res = requests.get(url.format(city)).json()
                city_weather.temp = res['main']['temp']
                city_weather.icon = res['weather'][0]['icon']
                city_weather.description = res['weather'][0]['description']
                city_weather.cod = res['cod']
                city_weather.save()
            except KeyError:
                context = {
                    'form': form,
                    'cod': res['cod'] == 404
                }
                city_weather.delete()
                return render(request, 'weather/weather.html', context)

        city_info = {
            'city': city,
            'temp': res["main"]["temp"],
            'icon': res['weather'][0]['icon']
        }
        form = CityReqForm()
        context = {
            'info': city_info,
            'form': form,
            'cod': res['cod'] != 404
        }
    else:
        if len(CityWeather.objects.all()) == 0:
            city = 'Vinica'
            res = requests.get(url.format(city)).json()
            city_info = {
                'city': city,
                'temp': res['main']['temp'],
                'icon': res['weather'][0]['icon']
            }
            form = CityReqForm()
            context = {
                'info': city_info,
                'form': form,
                'cod': res['cod'] != 404
            }
        else:
            city_weather = CityWeather.objects.order_by('-id')[0]
            city_info = {
                'city': city_weather.city_name,
                'temp': city_weather.temp,
                'icon': city_weather.icon
            }
            form = CityReqForm()
            context = {
                'info': city_info,
                'form': form,
                'cod': city_weather.cod != 404
            }
    return render(request, 'weather/weather.html', context)


def history(request):

    if request.method == 'POST':
        form = HistoryReqForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            hist = CityWeather.objects.order_by('-id')
            cod = 404
            paginator = Paginator(hist, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'form': form,
                'hist': hist,
                'title': 'История',
                'cod': cod==404,
                'page_obj': page_obj
            }
            return render(request, 'weather/history.html', context)

        try:
            history_req = HistoryReq.objects.order_by('-id')[0]
        except IndexError:
            cod = 404
            history_req = HistoryReq()

        try:
            if history_req.city == "All":
                hist = CityWeather.objects.raw("SELECT * FROM weather_cityweather WHERE date>=%s AND date<=%s",
                                              [history_req.date_from, history_req.date_to])
            else:
                hist = CityWeather.objects.raw("SELECT * FROM weather_cityweather WHERE date>=%s AND date<=%s AND city_name = %s",
                                               [history_req.date_from, history_req.date_to, history_req.city])
            cod = 200
        except ValueError:
            pass

        form = HistoryReqForm()
        paginator = Paginator(hist, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'form': form,
            'hist': hist,
            'title': 'История',
            'cod': cod == 404,
            'page_obj': page_obj
        }
        history_req.delete()
        return render(request, 'weather/history.html', context)

    form = HistoryReqForm()

    hist = CityWeather.objects.all()
    paginator = Paginator(hist, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'hist': hist,
        'title': 'История',
        'page_obj': page_obj
    }

    return render(request, 'weather/history.html', context)
