from django.template import Library
from utils import formatacao, get_qtd
register = Library()


@register.filter
def formata_preco(val):
    return formatacao.formata_preco(val)


@register.filter
def get_cart_qtd(carrinho):
    return get_qtd.get_cart_qtd(carrinho)

@register.filter
def cart_totals(carrinho):
    return get_qtd.cart_totals(carrinho)