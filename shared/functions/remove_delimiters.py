def remove_delimiters(text):
    # Remove os delimitadores '```' do início e fim do texto
    if text.startswith("```") and text.endswith("```"):
        return text[3:-3].strip()  # Retira os 3 primeiros e últimos caracteres
    return text
