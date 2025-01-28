def validate_dict(dict_to_validate, keys):
    if not isinstance(dict_to_validate, dict):
        raise ValueError("Inputs deve ser um dicionário.")
    required_keys = keys
    for key in required_keys:
        if key not in dict_to_validate:
            raise ValueError(f"Chave obrigatória '{key}' ausente em inputs.")
    return dict_to_validate
