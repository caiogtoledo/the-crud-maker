from functions_framework import http_function, HTTPResponse
from typing import Dict

@http_function()
def get_product_by_id(request: Dict) -> HTTPResponse:
    id = request.args.get('id')
    products = [
        {'id': 1, 'nome': 'Produto 1', 'preco': 10.99, 'descricao': 'Descrição do produto 1'},
        {'id': 2, 'nome': 'Produto 2', 'preco': 9.99, 'descricao': 'Descrição do produto 2'},
        {'id': 3, 'nome': 'Produto 3', 'preco': 12.99, 'descricao': 'Descrição do produto 3'}
    ]
    product = next((p for p in products if p['id'] == int(id)), None)
    if product:
        return HTTPResponse(body={'nome': product['nome'], 'preco': product['preco'], 'descricao': product['descricao']}, status_code=200)
    else:
        return HTTPResponse(body={'erro': 'Produto não encontrado'}, status_code=404)