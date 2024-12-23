from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentExecutor, AgentType
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re

load_dotenv()

groq_client = ChatGroq(model="llama-3.3-70b-versatile")

# Função para criar ou atualizar o arquivo Python


def create_or_update_py_file(file_name, content):
    try:
        with open(file_name, "w") as file:
            file.write(content)
        print(f"Arquivo {file_name} criado/atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao manipular o arquivo {file_name}: {e}")


def remove_delimiters(text):
    # Remove os delimitadores '```' do início e fim do texto
    if text.startswith("```") and text.endswith("```"):
        return text[3:-3].strip()  # Retira os 3 primeiros e últimos caracteres
    return text

# Função para gerar conteúdo da API


def get_model_response(prompt):
    """
    Função que faz a chamada ao modelo para obter uma resposta.

    :param prompt: Pergunta ou instrução para o modelo.
    :return: Resposta do modelo.
    """
    response = groq_client.invoke(prompt).content
    return response

# Função para criar a rota de API


def create_api_route():
    print("Bem-vindo ao criador de rotas de API! Responda as perguntas a seguir.")

    # Perguntas para o modelo
    input_data = input("Quais são os dados de entrada da rota?")
    input_data = "nome e senha"
    output_data = input("Quais são os dados de saída da rota?")
    output_data = "token de autenticação"
    business_rule = input("Qual é a regra de negócio da rota?")
    business_rule = "validar o usuário e senha e retornar um token de autenticação"
    storage_info = input("O que deve ser armazenado pela rota?")
    storage_info = "nenhum dado"

    # Prompt para o modelo gerar o código da rota
    route_prompt = f"""
    Create a  API route with Python and functions-framework of google with this specifications:
    - Entry data: {input_data}
    - Out data: {output_data}
    - Bussiness: {business_rule}
    - Storage rules: {storage_info}

    Use this rules inside tags <RULES>:
    <RULES>
     - Use the specifications that are provided
     - The response have to be ONLY code, without any text or comments before or after
    <RULES>

    Follow this example:

    """

    # Gerar conteúdo da API
    api_content = get_model_response(route_prompt)
    api_content = remove_delimiters(api_content)

    # Nome do arquivo gerado
    file_name = "generated_api.py"

    # Criar/atualizar arquivo
    create_or_update_py_file(file_name, api_content)

    print(f"Rota criada e salva em {file_name}!")


if __name__ == "__main__":
    create_api_route()
