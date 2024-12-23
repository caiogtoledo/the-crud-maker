import os
from langchain.chains import ConversationChain
from langchain.llms import HuggingFaceHub
from dotenv import load_dotenv

load_dotenv()

# Configuração do modelo da Hugging Face
llm = HuggingFaceHub(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    model_kwargs={"temperature": 0.2},
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

chat = ConversationChain(llm=llm)


def create_or_update_py_file(file_name, content):
    """
    Cria ou atualiza um arquivo Python com o conteúdo especificado.

    :param file_name: Nome do arquivo a ser criado ou atualizado.
    :param content: Conteúdo a ser escrito no arquivo.
    """
    try:
        with open(file_name, "w") as file:
            file.write(content)
        print(f"Arquivo {file_name} criado/atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao manipular o arquivo {file_name}: {e}")


def chat_sequence():
    """
    Função interativa que guia o usuário para criar uma rota de API usando LangChain.
    """
    print("Bem-vindo ao criador de rotas de API! Responda as perguntas a seguir.")

    # Usando o modelo de linguagem para obter informações do usuário
    input_data = chat.run("Qual os dados de entrada da rota?")
    output_data = chat.run("Qual os dados de saída da rota?")
    business_rule = chat.run("Qual é a regra de negócio da rota?")
    storage_info = chat.run("O que deve ser armazenado pela rota?")

    # Prompt para o modelo gerar o código da rota
    route_prompt = f"""
    Crie uma rota de API em Python utilizando Functions Framework com as seguintes especificações:
    - Dados de entrada: {input_data}
    - Dados de saída: {output_data}
    - Regra de negócio: {business_rule}
    - O que deve ser armazenado: {storage_info}
    """

    # Gerar conteúdo da API usando a LLM
    api_content = chat.run(route_prompt)

    # Nome do arquivo gerado
    file_name = "generated_api.py"

    # Criar/atualizar arquivo
    create_or_update_py_file(file_name, api_content)

    print(f"Rota criada e salva em {file_name}!")


if __name__ == "__main__":
    chat_sequence()
