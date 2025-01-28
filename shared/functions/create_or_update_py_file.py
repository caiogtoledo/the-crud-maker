# import os
# import ast

# # def create_or_update_py_file(folder_name: str, file_name: str, code: str):


# def create_or_update_py_file(data: dict):
#     try:
#         if 'folder_name' not in data or 'file_name' not in data or 'code' not in data:
#             return "Erro ao criar o arquivo: folder_name, file_name e code são obrigatórios no dicionário python e devem ser string."

#         data = data.replace("data=", "")
#         data = ast.literal_eval(data)

#         os.makedirs(data['folder_name'], exist_ok=True)

#         file_path = os.path.join(data['folder_name'], data['file_name'])

#         with open(file_path, "w") as file:
#             file.write(data['code'])
#         print(f"Arquivo {file_path} criado/atualizado com sucesso!")
#     except Exception as e:
#         print(f"Erro ao manipular o arquivo {data['file_name']}: {e}")


# DeepSeek code:

import os
import ast
from typing import Union, Dict, Any


def create_or_update_py_file(data: Union[Dict[str, Any], str]) -> str:
    """
    Cria ou atualiza um arquivo Python com conteúdo fornecido, garantindo validação e tratamento de erros.

    Args:
        data (dict | str): Dicionário ou string formatada como dicionário contendo:
            - folder_name: Nome da pasta (str)
            - file_name: Nome do arquivo (str)
            - content: Conteúdo do arquivo (str)

    Returns:
        str: Mensagem de sucesso ou erro
    """

    try:
        # Etapa 1: Converter e validar entrada
        if isinstance(data, str):
            # Remove possíveis prefixos (ex: 'data=', 'inputs=')
            data = data.split(
                '=', 1)[-1].strip() if '=' in data else data.strip()
            parsed_data = ast.literal_eval(data)
        elif isinstance(data, dict):
            parsed_data = data
        else:
            return "Erro: Entrada deve ser um dicionário ou string formatada como dicionário"

        # Etapa 2: Validação de estrutura
        required_keys = {'folder_name', 'file_name', 'content'}
        if not required_keys.issubset(parsed_data.keys()):
            missing = required_keys - parsed_data.keys()
            return f"Erro: Chaves obrigatórias faltando: {', '.join(missing)}"

        # Etapa 3: Limpeza e normalização
        folder_name = str(parsed_data['folder_name']).strip()
        file_name = str(parsed_data['file_name']).strip()

        # Garante extensão .py
        if not file_name.endswith('.py'):
            file_name += '.py'

        # Limpa conteúdo do arquivo
        content = parsed_data['content'].strip()
        content = content.replace("```python", "").replace("```", "").strip()

        # Etapa 4: Criação de diretórios
        try:
            os.makedirs(folder_name, exist_ok=True)
        except OSError as e:
            return f"Erro ao criar diretório: {str(e)}"

        # Etapa 5: Escrita do arquivo
        file_path = os.path.join(folder_name, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Verificação pós-escrita
        if not os.path.exists(file_path):
            return f"Erro: Arquivo {file_path} não foi criado"

        if os.path.getsize(file_path) == 0:
            return f"Aviso: Arquivo {file_path} foi criado vazio"

        return f"Sucesso: Arquivo {file_path} criado/atualizado"

    except (SyntaxError, ValueError) as e:
        return f"Erro de formatação: A entrada deve ser um dicionário Python válido - {str(e)}"
    except Exception as e:
        return f"Erro inesperado: {str(e)}"
