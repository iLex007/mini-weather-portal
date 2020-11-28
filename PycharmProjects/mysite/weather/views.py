from . models import CityWeather, HistoryReq, City
from django.shortcuts import render
import requests
from .forms import CityReqForm, HistoryReqForm
from django.core.paginator import Paginator
from django.views.generic import ListView


class HistoryView(ListView):
    form_class = HistoryReqForm
    initial = {'key': 'value'}
    template_name = 'weather/test.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        paginator = Paginator(CityWeather.objects.order_by('-date'), 5)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request, self.template_name, {'hist': CityWeather.objects.all(),
                                                    'form': form,
                                                    'title': 'История',
                                                    'page_obj': page_obj
                                                    })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            history_req = HistoryReq.objects.order_by('-id')[0]
            try:
                if history_req.city == "All":
                    hist = CityWeather.objects.raw("SELECT * "
                                                   "FROM weather_city as A "
                                                   "INNER JOIN weather_cityweather as B "
                                                   "ON A.city  = B.city_name_id "
                                                   "WHERE B.date>=%s AND B.date<=%s ",
                                                   [history_req.date_from, history_req.date_to])
                else:
                    hist = CityWeather.objects.raw("SELECT * "
                                                   "FROM weather_city as A "
                                                   "INNER JOIN weather_cityweather as B "
                                                   "ON A.city = B.city_name_id "
                                                   "WHERE B.date>=%s AND B.date<=%s AND A.city = %s",
                                                   [history_req.date_from, history_req.date_to, history_req.city])
                cod = 200
            except ValueError:
                cod = 404
            history_req.delete()

            paginator = Paginator(hist, 5)
            page_obj = paginator.get_page(request.GET.get('page'))
            return render(request, self.template_name, {'hist': hist,
                                                        'form': form,
                                                        'title': 'История',
                                                        'page_obj': page_obj,
                                                        'cod': cod == 404
                                                        })
        else:
            paginator = Paginator(CityWeather.objects.order_by('-date'), 5)
            page_obj = paginator.get_page(request.GET.get('page'))
            return render(request, self.template_name, {
                'hist': CityWeather.objects.order_by('-date'),
                'form': form,
                'cod': True,
                'title': 'История',
                'page_obj': page_obj
            })


class MainView(ListView):
    template_name = 'weather/weather.html'
    initial = {'key': 'value'}
    appid = '57bd238729c465144436fe7e688d6e2d'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    form_class = CityReqForm

    def get(self, request):
        if len(CityWeather.objects.all()) == 0:
            city = 'Vinica'
            res = requests.get(self.url.format(city)).json()
            city_info = {
                'city': city,
                'temp': res['main']['temp'],
                'icon': res['weather'][0]['icon']
            }
            form = self.form_class(initial=self.initial)
            context = {
                'info': city_info,
                'form': form,
                'cod': res['cod'] != 404
            }
        else:
            city_weather = CityWeather.objects.order_by('-id')[0]
            city_info = {
                'city': city_weather.city_name.city,
                'temp': city_weather.temp,
                'icon': city_weather.icon
            }
            form = self.form_class(initial=self.initial)
            context = {
                'info': city_info,
                'form': form,
                'cod': city_weather.cod != 404
            }

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        city_name = request.POST['city']
        city = City.objects.raw("SELECT * FROM weather_city WHERE city = %s", [city_name])[0]
        try:
            res = requests.get(self.url.format(city.city)).json()
            city_weather = CityWeather(city_name=city, temp=res['main']['temp'], icon=res['weather'][0]['icon'],
                                       description=res['weather'][0]['description'], cod=res['cod'])
            city_weather.save()
        except KeyError:
            context = {
                'form': self.form_class(initial=self.initial),
                'cod': res['cod'] == 404
            }
            city.delete()
            return render(request, self.template_name, context)
        city_info = {
            'city': city_weather.city_name.city,
            'temp': city_weather.temp,
            'icon': city_weather.icon
        }
        form = self.form_class(initial=self.initial)
        context = {
                'info': city_info,
                'form': form,
                'cod': city_weather.cod != 404
            }
        return render(request, 'weather/weather.html', context)

