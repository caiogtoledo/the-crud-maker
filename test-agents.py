from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# Inicializando o cliente ChatGroq
groq_client = ChatGroq(model="llama-3.3-70b-versatile")

# Função para interagir com o modelo e gerar a resposta


def get_model_response(prompt: str) -> str:
    response = groq_client.invoke(prompt)
    return response.content

# Função para criar ou atualizar arquivos Python


def create_or_update_py_file(file_name: str, content: str):
    with open(file_name, "w") as file:
        file.write(content)

# Ferramenta para coletar dados de entrada


def collect_inputs(*args, **kwargs):
    input_data = input("Quais são os dados de entrada da rota?")
    output_data = input("Quais são os dados de saída da rota?")
    business_rule = input("Qual é a regra de negócio da rota?")
    storage_info = input("O que deve ser armazenado pela rota?")
    return {"input_data": input_data, "output_data": output_data, "business_rule": business_rule, "storage_info": storage_info}

# Ferramenta para gerar o código da API


def generate_api_code(inputs):
    import ast
    print("inputs:", inputs)
    inputs = ast.literal_eval(inputs)
    prompt = f"""
    Create a  API route with Python and functions-framework of google with this specifications:
    - Entry data: {inputs['input_data']}
    - Out data: {inputs['output_data']}
    - Bussiness: {inputs['business_rule']}
    - Storage rules: {inputs['storage_info']}

    Use this rules inside tags <RULES>:
    <RULES>
     - Use the specifications that are provided
     - The response have to be ONLY code, without any text or comments before or after
    <RULES>
    """
    return get_model_response(prompt)

# Ferramenta para salvar o código gerado


def save_generated_code(code):
    file_name = "generated_api.py"
    create_or_update_py_file(file_name, code)
    return f"Rota criada e salva em {file_name}!"


# Definição das ferramentas para o agente
tools = [
    Tool(
        name="Coletar Entradas",
        func=collect_inputs,
        description="Coleta as entradas necessárias para gerar uma rota de API."
    ),
    Tool(
        name="Gerar Código de API",
        func=generate_api_code,
        description="Gera o código da rota da API com base nas entradas fornecidas."
    ),
    Tool(
        name="Salvar Código Gerado",
        func=save_generated_code,
        description="Salva o código gerado em um arquivo Python."
    )
]

# Inicializando o agente
agent = initialize_agent(
    tools, groq_client, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Execução principal
if __name__ == "__main__":
    print("Bem-vindo ao criador de rotas de API!")
    # Coletar entradas
    inputs = agent.invoke(
        "Coletar os dados de entrada necessários para gerar a API.")
    # Gerar código da API
    generated_code = agent.invoke(
        f"Gerar o código da API com as especificações coletadas: {inputs}")
    # Salvar o código
    result = agent.invoke(
        f"Salvar o código gerado no arquivo: {generated_code}")
    print(result)
