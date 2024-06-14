from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpRequest, HttpResponse
from .models import Produto, Variacao
from pprint import pprint

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
        # if self.request.session.get('carrinho'):
        #     del self.request.session['carrinho']
        #     self.request.session.save()
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:ListarProdutos'))
        variacao_id = self.request.POST.get('vid')
        variacao_id_str = str(variacao_id)  # Convertendo variacao_id para string para usar como chave no dicionário
        print(f"Variacao ID recebido: {variacao_id_str}")  # Linha de debug
        
        if not variacao_id:
            messages.error(self.request, 'Produto não encontrado')
            return redirect(http_referer)
        
        variacao = get_object_or_404(Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id # type: ignore
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        # imagem = produto.imagem

        if variacao_estoque < 1:
            messages.error(self.request, 'Estoque insuficiente')
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}

        carrinho = self.request.session['carrinho']
        print(f"Carrinho antes de adicionar: {carrinho}")  # Linha de debug

        if variacao_id_str in carrinho:
            quantidade_carrinho = carrinho[variacao_id_str]['quantidade']
            quantidade_carrinho += 1
            print(f"Quantidade no carrinho antes de atualizar: {quantidade_carrinho}")  # Linha de debug

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                    f'no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id_str]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id_str]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id_str]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
        else:
            carrinho[variacao_id_str] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                # 'imagem': imagem,
            }

        # Certifique-se de que o carrinho atualizado seja salvo na sessão
        self.request.session['carrinho'] = carrinho
        self.request.session.modified = True  # Marcar a sessão como modificada
        # self.request.session.save()  # Removido

        print(f"Carrinho depois de adicionar: {carrinho}")  # Linha de debug

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu '
            f'carrinho {carrinho[variacao_id_str]["quantidade"]}x.'
        )
        pprint(carrinho)
        return HttpResponse(f'variacao: {variacao.nome}')

class RemoverDoCarrinho(View):
    pass



class Carrinho(View):
    pass



class FinalizarCompra(View):
    pass