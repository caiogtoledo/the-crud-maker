```python
from functions_framework import http_function
from flask import jsonify

users = {
    1: {"nome": "Joao", "idade": 30, "email": "joao@example.com"},
    2: {"nome": "Maria", "idade": 25, "email": "maria@example.com"},
}

@http_function
def get_user(request):
    id_usuario = int(request.args.get("id"))
    if id_usuario in users:
        return jsonify(users[id_usuario])
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404
```