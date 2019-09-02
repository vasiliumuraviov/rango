from django.urls import path

from . import views

app_name = 'rango_core'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show-category'),
    path('category/<slug:category_name_slug>/add-page/', views.add_page, name='add-page'),
    path('add-category/', views.add_category, name='add-category'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('restricted/', views.restricted, name='restricted'),

]
