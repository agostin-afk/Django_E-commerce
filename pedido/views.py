from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from produto.models import Variacao
from .models import Pedido, ItemPedido
from utils.get_qtd import get_cart_qtd, cart_totals
from django.urls import reverse


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args: Any, **kwargs: Any):
        if not self.request.user.is_authenticated:
            return redirect('perfil:CreateUser')
        return super().dispatch(*args, **kwargs)
    def get_queryset(self, *args, **kwargs):
        qs= super().get_queryset(*args, **kwargs) # type: ignore
        qs = qs.filter(usuario=self.request.user)
        return qs

class Pagar(DispatchLoginRequiredMixin, DetailView):
    template_name= 'pedido/pagar.html'
    model= Pedido
    pk_url_kwarg= 'pk'
    context_object_name= 'pedido'
    


class FecharPedido(View):
    template_name='pedido/pagar.html'
    def get(self, *args, **kwargs):
        
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer o login.'
            )
            return redirect('perfil:CreateUser')
        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio'
            )
            return redirect('produto:ListarProdutos')
        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho] # type: ignore
        db_variacoes = list(Variacao.objects.select_related('produto').filter(id__in=carrinho_variacao_ids))
        for variacao in  db_variacoes:
            vid = str(variacao.id)# type: ignore
            estoque= variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']# type: ignore
            preco_unt = carrinho[vid]['preco_unitario']# type: ignore
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']# type: ignore
            
            error_msg_estoque = ''
            
            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque# type: ignore
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt# type: ignore
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo# type: ignore
                error_msg_estoque = 'Estoque insuficiente para alguns produtos no seu carrinho.'
                
            if error_msg_estoque:
                messages.error(
                    self.request,
                    'Estoque insuficiente para alguns produtos no seu carrinho.'
                )
                self.request.session.save()
                return redirect('produto:Carrinho')
        qtd_total_carrinho = get_cart_qtd(carrinho)
        valor_total_carrinho = cart_totals(carrinho)
        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )
        pedido.save()
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()# type: ignore
            ]
        )
        contexto = {
            
        }
        del self.request.session['carrinho']
        return redirect(
            reverse(
                'pedido:Pagar',
                kwargs={
                    'pk': pedido.pk,
                }
            )
        )



class Detalhe(DispatchLoginRequiredMixin, DetailView):
    model= Pedido
    context_object_name= 'pedido'
    template_name= 'pedido/detalhe.html'
    pk_url_kwarg='pk'
class ListaPedidos(DispatchLoginRequiredMixin, ListView):
    model= Pedido
    context_object_name= 'pedidos'
    template_name= 'pedido/lista_pedido.html'
    paginate_by= 10
    ordering= ['-id']