from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('last', views.last),
    path('yesterday', views.yesterday),
    path('today', views.today),
]