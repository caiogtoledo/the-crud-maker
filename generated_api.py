python
from functions_framework import httplib
from flask import request, jsonify
import jwt
import time

def authenticate_user(nome, senha):
    # Simulating a user database for demonstration purposes
    users = {
        "user1": "password1",
        "user2": "password2"
    }
    
    if nome in users and users[nome] == senha:
        return True
    else:
        return False

def generate_token(nome):
    payload = {
        'nome': nome,
        'exp': int(time.time()) + 3600
    }
    return jwt.encode(payload, 'secret_key', algorithm='HS256')

@httplib.HTTP
def entry(request):
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')
    
    if authenticate_user(nome, senha):
        token = generate_token(nome)
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401