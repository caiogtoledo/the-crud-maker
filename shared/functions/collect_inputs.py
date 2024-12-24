def collect_inputs(*args, **kwargs):
    input_data = input("Quais são os dados de entrada da rota?")
    output_data = input("Quais são os dados de saída da rota?")
    business_rule = input("Qual é a regra de negócio da rota?")
    storage_info = input("O que deve ser armazenado pela rota?")
    return {"input_data": input_data, "output_data": output_data, "business_rule": business_rule, "storage_info": storage_info}
