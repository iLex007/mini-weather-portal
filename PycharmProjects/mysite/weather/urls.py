from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('history', views.history, name='history'),
    path("test", views.MainView.as_view()),
]
