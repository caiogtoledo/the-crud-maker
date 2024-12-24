```python
from functions_framework import http_function, HTTPResponse
from typing import Dict

products: Dict[str, Dict] = {
    "1": {"nome": "Produto 1", "descrição": "Descrição do produto 1", "preço": 10.99},
    "2": {"nome": "Produto 2", "descrição": "Descrição do produto 2", "preço": 9.99},
    "3": {"nome": "Produto 3", "descrição": "Descrição do produto 3", "preço": 12.99}
}

@http_function
def get_product(request):
    id = request.args.get("id")
    if id in products:
        return HTTPResponse(body=products[id], status_code=200, headers={"Content-Type": "application/json"})
    else:
        return HTTPResponse(body={"mensagem": "Produto não encontrado"}, status_code=404, headers={"Content-Type": "application/json"})
```