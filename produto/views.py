from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpRequest, HttpResponse
from .models import Produto, Variacao


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
    def post(self, request, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:ListarProdutos'))
        variacao_id = self.request.POST.get('vid')
        
        if not variacao_id:
            messages.error(self.request, 'Produto não encontrado')
            return redirect(http_referer)
        variacao = get_object_or_404(Variacao, id=variacao_id)
        messages.success(self.request, 'Produto adicionado ao carrinho')
        
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
        carrinho = self.request.session['carrinho']
        
        if variacao_id in carrinho:
            pass
        else:
            pass
        return HttpResponse(f'variacao: {variacao.nome}')
class RemoverDoCarrinho(View):
    pass



class Carrinho(View):
    pass



class FinalizarCompra(View):
    pass