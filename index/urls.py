from django.urls import path

from index import views

app_name = 'index'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('get_buys/', views.get_buys, name='get_buys'),
    path('get_sells/', views.get_sells, name='get_sells'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell'),
    path('transactions/', views.transactions, name='transactions'),
    path('get_transactions/', views.get_transactions, name='get_transactions'),
    path('transactions_buy/', views.transactions_buy, name='transactions_buy'),
]
