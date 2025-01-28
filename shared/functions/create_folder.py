import os
import ast


def create_folder(data: dict):
    try:
        if 'folder_name' not in data:
            return "Erro ao criar a pasta api: folder_name é obrigatório no dicionário python e deve ser uma string."
        data = data.replace("data=", "")
        data = ast.literal_eval(data)
        os.mkdir(data['folder_name'])
        print(f"Pasta {data['folder_name']} criada com sucesso!")
    except Exception as e:
        return f"""Erro ao criar a pasta api: {
            e}\n Tente novamente enviando um formato válido. Ex: {'folder_name': 'get_produto'}"""
