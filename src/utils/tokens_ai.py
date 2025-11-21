import tiktoken

def contar_tokens(texto: str, modelo: str = "gpt-4.1"):
    """
    Retorna la cantidad de tokens que usa un texto según el modelo elegido.
    """
    try:
        encoding = tiktoken.encoding_for_model(modelo)
    except KeyError:
        # Si el modelo no está registrado, usa cl100k_base (compatible con GPT-4 y GPT-3.5)
        encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens = encoding.encode(texto)
    return len(tokens)

def calcular_costo(tokens_entrada: int, tokens_salida: int,
                   precio_por_millón_entrada: float,
                   precio_por_millón_salida: float) -> float:
    """
    Calcula el costo estimado en US$ dado el número de tokens
    de entrada y salida, y los precios por millón de tokens.
    """
    precio_token_entrada = precio_por_millón_entrada / 1_000_000
    precio_token_salida  = precio_por_millón_salida  / 1_000_000

    costo = tokens_entrada * precio_token_entrada \
           + tokens_salida * precio_token_salida
    return costo