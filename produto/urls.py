from django.urls import path
from .views import *

app_name = 'produto'
urlpatterns = [
    path('', ListarProdutos.as_view(), name='ListarProdutos'),
    path('<slug:slug>/', DetalheProduto.as_view(), name='DetalheProduto'),
    path('AddItemCart/', AdicionarAoCarrinho.as_view(), name='AdicionarAoCarrinho'),
    path('RemoveItemCart/', RemoverDoCarrinho.as_view(), name='RemoverDoCarrinho'),
    path('Cart', Carrinho.as_view(), name='Carrinho'),
    path('Checkout/', FinalizarCompra.as_view(), name='FinalizarCompra'),
]