from django.urls import path
from . import views

app_name = 'rango_core'

urlpatterns = [
    path('', views.index, name='rango-core-index'),
    path('about/', views.about, name='rango-core-about')
]
