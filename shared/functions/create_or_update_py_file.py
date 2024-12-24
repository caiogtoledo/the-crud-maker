def create_or_update_py_file(file_name: str, content: str):
    try:
        with open(file_name, "w") as file:
            file.write(content)
        print(f"Arquivo {file_name} criado/atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao manipular o arquivo {file_name}: {e}")
