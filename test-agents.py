from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from shared.functions.collect_inputs import collect_inputs
from shared.functions.create_folder import create_folder
from shared.functions.create_or_update_py_file import create_or_update_py_file
from shared.functions.get_model_response import get_model_response
from shared.functions.validate_dict import validate_dict

from shared.functions.clean_archtecture.generate_controller import generate_controller
from shared.functions.clean_archtecture.generate_presenter import generate_presenter
# from shared.functions.clean_archtecture.generate_usecase import generate_usecase
# from shared.functions.clean_archtecture.generate_viewmodel import generate_viewmodel

load_dotenv()
print(os.getenv("GROQ_API_KEY"))

# Inicializando o cliente ChatGroq
groq_client = ChatGroq(model="llama-3.3-70b-specdec",
                       api_key=os.getenv("GROQ_API_KEY"))

# Ferramenta para gerar o código da API


def generate_api_code(inputs):
    import ast
    print("inputs:", inputs)
    inputs = inputs.replace("inputs=", "")
    try:
        inputs = validate_dict(ast.literal_eval(inputs), [
            "input_data", "output_data", "business_rule", "storage_info"])
    except Exception as e:
        return "Erro ao validar a resposta do modelo: {e}, tente novamente sem alterar o conteúdo gerado."

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
    response = get_model_response(groq_client, prompt).replace(
        "```python", "").replace("```", "")
    return response


# Definição das ferramentas para o agente
tools = [
    Tool(
        name="Coletar Entradas",
        func=collect_inputs,
        description="Coleta as entradas necessárias para gerar uma rota de API."
    ),
    # TODO - Criar uma pasta específica para cada rota
    Tool(
        name="Criar Pasta",
        func=create_folder,
        description="Cria uma pasta para armazenar os arquivos gerados para a API."
    ),
    # TODO - Criar uma tool para cada arquivo necessário
    # Tool(
    #     name="Gerar Código de API",
    #     func=generate_api_code,
    #     description="Gera o código da rota da API com base nas entradas fornecidas."
    # ),
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
        name="Salvar Código Gerado",
        func=create_or_update_py_file,
        description="Salva o código gerado em um arquivo Python e pasta especificada."
    )
]

tasks = {
    'colect': PromptTemplate.from_template("Coletar os dados de entrada necessários para gerar a API."),
    'create_folder': PromptTemplate.from_template(""" 
                        Criar a pasta {folder_name} para armazenar os arquivos gerados para API. 
                        Sempre em inglês, snake_case, sem espaços e o nome com relação a funcionalidade principal da rota.
                    """),

    # 'generate_entity': PromptTemplate.from_template("Gerar a entidade da API com as especificações coletadas: {inputs}"),
    # 'save_entity': PromptTemplate.from_template("Salvar o código da entidade gerada: {generated_code_entity} no arquivo: {entity_file_name}"),

    # 'generate_repository': PromptTemplate.from_template("Gerar o repository da API com as especificações coletadas: {inputs}"),
    # 'save_repository': PromptTemplate.from_template("Salvar o repository gerado: {generated_code_repository} no arquivo: {repository_file_name}"),

    # 'generate_viewmodel': PromptTemplate.from_template("Gerar o viewmodel da API com as especificações coletadas: {inputs}"),
    # 'save_viewmodel': PromptTemplate.from_template("Salvar o viewmodel gerado: {generated_code_viewmodel} no arquivo: {viewmodel_file_name}"),

    # 'generate_usecase': PromptTemplate.from_template("Gerar o usecase da API com as especificações coletadas: {inputs}"),
    # 'save_usecase': PromptTemplate.from_template("Salvar o usecase gerado: {generated_code_usecase} no arquivo: {usecase_file_name}"),

    'generate_controller': PromptTemplate.from_template("Gerar o codigo em python do controller da API com as especificações coletadas: {inputs}. Salve no arquivo {file_name} na pasta {folder_name} o código final {content}"),
    # 'save_controller': PromptTemplate.from_template("Salvar o controller gerado: {generated_code_controller}\n Salve no arquivo {controller_file_name} que deve ser salvo dentro da pasta {folder_name}"),

    'generate_presenter': PromptTemplate.from_template("Gerar o codigo em python do presenter da API com as especificações coletadas: {inputs}. Salve no arquivo {file_name} na pasta {folder_name} o código final {content}"),
    # 'save_presenter': PromptTemplate.from_template("Salvar o presenter gerado: {generated_code_presenter} no arquivo: {presenter_file_name} que deve ser salvo dentro da pasta {folder_name}"),

    # 'generate_all_tests': PromptTemplate.from_template("Gerar todos os testes da API que foi gerada, criar um arquivo para cada camada também"),
    # 'save__all_tests': PromptTemplate.from_template("Salvar todos os testes gerados em arquivos separados"),

    'conference': PromptTemplate.from_template("Confiro se eu realmente gerei todos os arquivos necessários para a API e salvei na pasta que foi determinada."),
}

# Inicializando o agente
agent = initialize_agent(
    tools, groq_client, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Execução principal
if __name__ == "__main__":
    # chain = tasks['colect'] | tasks['create_folder'] | tasks['generate_controller'] | tasks["save_controller"]
    chain = tasks['colect'] | tasks['create_folder'] | tasks['generate_controller'] | tasks['generate_presenter'] | tasks['conference']
    result = agent.invoke(chain)
    print(result)
