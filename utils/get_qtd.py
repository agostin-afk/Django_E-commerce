def get_cart_qtd(carrinho):
    return sum(item['quantidade'] for item in carrinho.values())