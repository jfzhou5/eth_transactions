from django.urls import path

from stock import views

app_name = 'ipo'

urlpatterns = [
    path('index/', views.ipo_index, name='ipo_index'),
    path('get_list/', views.get_list, name='get_list'),
    path('ipo_submit/', views.ipo_submit, name='ipo_submit'),
]