from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentExecutor, AgentType
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re

from shared.functions import create_or_update_py_file, get_model_response, remove_delimiters

load_dotenv()

groq_client = ChatGroq(model="llama-3.3-70b-specdec",
                       api_key=os.getenv("GROQ_API_KEY"))


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
