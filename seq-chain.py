from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

groq_client = ChatGroq(model="llama-3.3-70b-specdec",
                       api_key=os.getenv("GROQ_API_KEY"))

# Definição das tarefas como LLMChains
collect_inputs_chain = LLMChain(llm=groq_client, prompt=PromptTemplate.from_template(
    "Coletar os dados de entrada necessários para gerar a API."))
create_folder_chain = LLMChain(llm=groq_client, prompt=PromptTemplate.from_template(
    "Criar a pasta {folder_name} para armazenar os arquivos gerados para API."))
generate_controller_chain = LLMChain(llm=groq_client, prompt=PromptTemplate.from_template(
    "Gerar o codigo em python do controller da API com as especificações coletadas: {inputs}."))
generate_presenter_chain = LLMChain(llm=groq_client, prompt=PromptTemplate.from_template(
    "Gerar o codigo em python do presenter da API com as especificações coletadas: {inputs}."))

# Criação da SequentialChain
sequential_chain = SequentialChain(
    chains=[collect_inputs_chain, create_folder_chain,
            generate_controller_chain, generate_presenter_chain],
    input_variables=["inputs", "folder_name"],
    verbose=True
)

# Execução principal
if __name__ == "__main__":
    inputs = {"input_data": "example_input", "output_data": "example_output",
              "business_rule": "example_rule", "storage_info": "example_storage"}
    folder_name = "example_folder"
    result = sequential_chain.run(inputs=inputs, folder_name=folder_name)
    print(result)
