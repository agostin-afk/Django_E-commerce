from django.urls import path
from .views import *

app_name= 'pedido'

urlpatterns = [
    path('Pagar/<int:pk>', Pagar.as_view(), name='Pagar'),
    path('FecharPedido/', FecharPedido.as_view(), name='FecharPedido'),
    path('Lista/', ListaPedidos.as_view(), name='ListaPedidos'),
    path('Detalhe/<int:pk>', Detalhe.as_view(), name='Detalhe'),
]