from django.urls import path
from .views import *

app_name = 'produto'
urlpatterns = [
    path('', ListarProdutos.as_view(), name='ListarProdutos'),
    path('produto/<slug:slug>/', DetalheProduto.as_view(), name='DetalheProduto'),
    path('addItemCart/', AdicionarAoCarrinho.as_view(), name='AdicionarAoCarrinho'),
    path('removeItemCart/', RemoverDoCarrinho.as_view(), name='RemoverDoCarrinho'),
    path('cart', Carrinho.as_view(), name='Carrinho'),
    path('checkout/', FinalizarCompra.as_view(), name='FinalizarCompra'),
    path('busca/', Busca.as_view(), name='Busca'),
]