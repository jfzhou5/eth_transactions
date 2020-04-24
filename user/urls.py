from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('stock/', views.user_stock, name='user_stock'),
    path('login/', views.login, name='login'),
    path('check_user/', views.check_user, name='check_user'),
    path('login_form/', views.login_form, name='login_form'),
    path('register/', views.register, name='register'),
    path('register_form/', views.register_form, name='register_form'),
    path('get_list/', views.get_list, name='get_list'),
    path('sell/', views.sell, name='sell'),

]