from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages


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
        contexto = {
            
        }
        return render(self.request, self.template_name, contexto)


class SalvarPedido(View):
    pass

class FecharPedido(View):
    pass


class Detalhe(View):
    pass