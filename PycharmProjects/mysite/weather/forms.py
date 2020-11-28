from .models import *
from django.forms import ModelForm, TextInput, DateTimeInput
from django_select2 import forms as s2forms


class CityReqForm(ModelForm):
    class Meta:
        model = City
        fields = ['city']
        widgets = {
                'city_name': TextInput(attrs={
                'class': 'for-control',
                'placeholder': "Введите название города",
                'style': "width: 250px;"
            })
        }


class HistoryReqForm(ModelForm):
    class Meta:
        model = HistoryReq
        fields = ['city', 'date_from', 'date_to']
        widgets = {
            'city': TextInput(attrs={
                'class': 'for-control',
                'placeholder': "Введите город",
                'style': "width: 250px"
            }),
            'date_from': DateTimeInput(attrs={
                'class': 'for-control',
                'placeholder': "Введите дату начала",
                'style': "width: 250px"
            }),
            'date_to': DateTimeInput(attrs={
                'class': 'for-control',
                'placeholder': "Введите дату конца",
                'style': "width: 250px"
            })
        }


class CityWidget(s2forms.ModelSelect2Widget):
    search_fields = ['city_name']

