def get_model_response(client, prompt):
    """
    Função que faz a chamada ao modelo para obter uma resposta.

    :param prompt: Pergunta ou instrução para o modelo.
    :return: Resposta do modelo.
    """
    response = client.invoke(prompt).content
    return response
