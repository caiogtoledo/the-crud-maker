from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from shared.functions.collect_inputs import collect_inputs
from shared.functions.create_or_update_py_file import create_or_update_py_file
from shared.functions.get_model_response import get_model_response

load_dotenv()

# Inicializando o cliente ChatGroq
groq_client = ChatGroq(model="llama-3.3-70b-versatile")

# Ferramenta para gerar o código da API


def generate_api_code(inputs):
    import ast
    print("inputs:", inputs)
    inputs = inputs.replace("inputs=", "")
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
    return get_model_response(groq_client, prompt).replace("```python", "").replace("```", "")

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
    # TODO - Criar uma pasta específica para cada rota
    # TODO - Criar uma tool para cada arquivo necessário
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

tasks = {
    'colect': PromptTemplate.from_template("Coletar os dados de entrada necessários para gerar a API."),
    'generate_code': PromptTemplate.from_template("Gerar o código da API com as especificações coletadas: {inputs}"),
    'save': PromptTemplate.from_template("Salvar o código gerado no arquivo: {generated_code}")
}

# Inicializando o agente
agent = initialize_agent(
    tools, groq_client, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Execução principal
if __name__ == "__main__":
    chain = tasks['colect'] | tasks['generate_code'] | tasks['save']
    result = agent.invoke(chain)
    print(result)
