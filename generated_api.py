from functions_framework import http_function
from flask import jsonify

produtos = [
    {"id": 1, "nome": "Produto 1", "descricao": "Descrição do produto 1", "preco": 10.99},
    {"id": 2, "nome": "Produto 2", "descricao": "Descrição do produto 2", "preco": 9.99},
    {"id": 3, "nome": "Produto 3", "descricao": "Descrição do produto 3", "preco": 12.99}
]

@http_function
def get_produto(request):
    id = int(request.args.get('id'))
    produto = next((p for p in produtos if p['id'] == id), None)
    if produto:
        return jsonify(produto)
    else:
        return jsonify({"mensagem": "Produto não encontrado"}), 404