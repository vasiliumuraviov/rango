from django.urls import path, include
from . import views

app_name = 'rango_core'

urlpatterns = [
    path('', views.index, name='index'),
]
