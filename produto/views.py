from typing import Any
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpRequest, HttpResponse
from .models import Produto


class ListarProdutos(ListView):
    model= Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by= 9



class DetalheProduto(DetailView):
    model= Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarAoCarrinho(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse("AdicionarAoCarrinho")



class RemoverDoCarrinho(View):
    pass



class Carrinho(View):
    pass



class FinalizarCompra(View):
    pass