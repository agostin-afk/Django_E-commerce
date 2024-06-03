from django.urls import path
from .views import *

app_name= 'pedido'

urlpatterns = [
    path('Pagar/', Pagar.as_view(), name='Pagar'),
    path('FecharPedido/', FecharPedido.as_view(), name='FecharPedido'),
    path('Detalhe/<int:pk>', Detalhe.as_view(), name='Detalhe'),
]
