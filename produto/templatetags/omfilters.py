from django.template import Library
from utils import formatacao 
register = Library()


@register.filter
def formata_preco(val):
    return formatacao.formata_preco(val)
