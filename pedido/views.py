from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao


class Pagar(View):
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
        carrinho_variacao_ids = [v for v in carrinho]
        db_variacoes = list(Variacao.objects.select_related('produto').filter(id_in=carrinho_variacao_ids))
        for variacao in  db_variacoes:
            vid = str(variacao.id)
            estoque= variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']
            
            error_msg_estoque = ''
            
            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo
                error_msg_estoque = 'Estoque insuficiente para alguns produtos no seu carrinho.'
                
            if error_msg_estoque:
                messages.error(
                    self.request,
                    'Estoque insuficiente para alguns produtos no seu carrinho.'
                )
                self.request.session.save()
                return redirect('produto:Carrinho')
            
        contexto = {
            
        }
        return render(self.request, self.template_name, contexto)


class SalvarPedido(View):
    pass

class FecharPedido(View):
    pass


class Detalhe(View):
    pass