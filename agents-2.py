from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from shared.functions.clean_archtecture.generate_controller import generate_controller
from shared.functions.clean_archtecture.generate_presenter import generate_presenter
from shared.functions.collect_inputs import collect_inputs
from shared.functions.create_folder import create_folder
from shared.functions.create_or_update_py_file import create_or_update_py_file

import os

load_dotenv()

# Definição das ferramentas
tools = [
    Tool(
        name="Coletar Entradas",
        func=collect_inputs,
        description="Coleta as entradas necessárias para gerar uma rota de API."
    ),
    Tool(
        name="Criar Pasta",
        func=create_folder,
        description="Cria uma pasta para armazenar os arquivos gerados para a API."
    ),
    Tool(
        name="Gerar Controller",
        func=generate_controller,
        description="Gera o controller da API com base nas entradas fornecidas."
    ),
    Tool(
        name="Gerar Presenter",
        func=generate_presenter,
        description="Gera o presenter da API com base nas entradas fornecidas."
    ),
    Tool(
        name="Salvar Código",
        func=create_or_update_py_file,
        description="Salva o código gerado em um arquivo Python em uma pasta específica."
    )
]

groq_client = ChatGroq(model="llama-3.3-70b-specdec",
                       api_key=os.getenv("GROQ_API_KEY"))

# Inicialização do agente
agent = initialize_agent(
    tools, groq_client, agent="zero-shot-react-description", verbose=True)

# Execução principal
if __name__ == "__main__":
    result = agent.invoke(
        """
        Você é um engenheiro de software e precisa criar uma rota do CRUD para uma aplicação web.
        Siga o seguinte passo a passo:
        - Coletar entradas 
        - Criar pasta com nome de acordo com a ação do CRUD (get_..., create_..., update_... ou delete_...)
        - Gerar código python do controller com as especificações coletadas
        - Use a ferramenta "Salvar Código" para salvar o código do controller que foi gerado em um arquivo do controller (controller.py)
        - Gerar código python do presenter com as especificações coletadas
        - Use a ferramenta "Salvar Código" para salvar o código do presenter que foi gerado em um arquivo do presenter (presenter.py)
        """)
    print(result)
