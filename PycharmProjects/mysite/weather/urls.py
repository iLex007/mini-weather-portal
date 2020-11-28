from django.urls import path, include
from . import views


urlpatterns = [
    path('history', views.HistoryView.as_view(), name='history'),
    path('', views.MainView.as_view(), name='home'),
]
