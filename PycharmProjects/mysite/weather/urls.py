from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('history', views.history, name='history'),
    path("select2/", include("django_select2.urls")),
]
