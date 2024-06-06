from typing import Any
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpRequest, HttpResponse


class ListarProdutos(ListView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse("Listar")



class DetalheProduto(View):
    pass



class AdicionarAoCarrinho(View):
    pass



class RemoverDoCarrinho(View):
    pass



class Carrinho(View):
    pass



class FinalizarCompra(View):
    pass