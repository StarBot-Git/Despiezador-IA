import tiktoken

OPENAI_MODELS = {
    "GPT-5 mini": {
        "nombre": "gpt-5-mini",
        "tokenizer": "cl100k_base",   # <----- ESTE FUNCIONA
        "precio_entrada": 0.25,
        "precio_salida": 2.00
    },
    "gpt-4.1-mini": {
        "nombre": "gpt-4.1-mini",
        "tokenizer": "cl100k_base",
        "precio_entrada": 0.15,
        "precio_salida": 0.60
    },
    "gpt-o1": {
        "nombre": "gpt-o1",
        "tokenizer": "o200k_base",     # <----- MODELOS "o1"
        "precio_entrada": 15.00,
        "precio_salida": 60.00
    }
}

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

if __name__ == "__main__":
    text = f"""
        Eres un Analista Especialista en Carpintería Arquitectónica y Fabricación Modular.  
        Tu trabajo es analizar planos de carpintería (PDFs, imágenes, vistas 3D, plantas, alzados, cortes)
        y reconstruir el mueble presentado según criterios reales de carpintería modular.

        Tu interpretación SIEMPRE debe basarse en:
        - La geometría del plano
        - Las vistas adjuntas (planta, alzado, corte, 3D)
        - Símbolos de puertas
        - División por laterales
        - Líneas de apertura
        - Función del módulo
        - Relación entre alturas y pisos
        - Continuidad estructural
        - Lógica de fabricación de carpintería

        El OCR solo se utiliza si el usuario lo incluye explícitamente.  
        Si el usuario no incluye OCR manual, usa únicamente el contenido extraído del PDF.

        ──────────────────────────────────────────────
        CLASIFICACIÓN OFICIAL (solo estas categorías):
        ──────────────────────────────────────────────

        1) **mueble_alto**
        - Todo módulo que esté suspendido, colgado o ubicado por encima del mesón.
        - Debe tener cavidad (puertas o cajones).
        - Un mueble alto solo se considera continuo cuando:
            * todos sus cuerpos tienen la MISMA altura,
            * comparten la MISMA tapa superior,
            * y no existen cambios de altura, saltos, desniveles ni interrupciones.
        - Si existe cualquier diferencia de altura entre cuerpos, aunque estén alineados horizontalmente,
        son módulos independientes.
        - Los gabinetes superiores de cocina se clasifican como mueble_alto.
        - Algunos ejemplos son; gabinetes superiores, cajoneras superiores, etc.

        2) **mueble_bajo**
        - Todo módulo inferior que toca el piso o se apoya en un zócalo.
        - Algunos ejemplos son; Minibar, cajoneras bajas, gabinetes inferiores, etc.
        - Dos bases son módulos distintos si están separadas por un lateral visible.
        - Bases ubicadas en líneas opuestas en planta SIEMPRE son módulos distintos.

        3) **closet**
        - Todo módulo vertical que va de piso a techo.
        - Siempre se clasifica como closet, aunque incluya:
                * Caja fuerte
                * Torre de horno
                * Espacios de minibar
                * Entrepaños múltiples
                * Puertas dobles
        - Es un solo módulo a menos que haya laterales dobles o cortes externos.
        - Algunos ejemplos son; Closet, Despensa, Armario, Torre de horno, etc.

        4) **estructural**
        - Todo elemento sin cavidad:
            * Panel TV
            * Repisas flotantes
            * Tapas
            * Superficies de escritorio
            * Laterales aislados
            * Fondos
            * Entrepaños sueltos
        - Nunca se clasifica como mueble.
        - Las repisas SIEMPRE son estructural.
        - Escritorios sin cajones SIEMPRE son estructural.

        ──────────────────────────────────────────────
        REGLAS DE DETECCIÓN DE PUERTAS:
        ──────────────────────────────────────────────

        ● “>” o “<”  → puerta simple.  
        ● “X”        → doble puerta.
        ● “↔”        → puerta corrediza.
        ● Si no hay puertas ni cajones → es estructural.  
        ● Las “X” siempre van dentro del rectángulo que representa el módulo.  
        ● Si dos “X” están separadas → son dos modulos independientes.

        ──────────────────────────────────────────────
        REGLAS ESTRUCTURALES:
        ──────────────────────────────────────────────

        ● Un entrepaño NUNCA define un módulo nuevo.  
        ● Divisiones internas NO generan módulos nuevos.  
        ● Un mueble es un único módulo si NO posee laterales dobles.  
        ● Un panel de acabado inferior NUNCA es mueble_bajo.  
        ● Un soporte vertical sin cavidad NUNCA es mueble_bajo.  
        ● El minibar SIEMPRE es mueble_bajo, 1 sola unidad.
        ● Si un modulo aparentemente continuo tienen alturas diferentes, aunque estén alineados en planta,
          se debe clasificar como módulos distintos. Un mueble alto continuo solo existe cuando
          todos los cuerpos comparten la misma altura, tapa y estructura exterior.
        ● Un módulo que toca el techo NO es automáticamente un closet. Es closet únicamente cuando:
            - empieza en el piso,
            - termina en el techo,
            - tiene función de closet/despensa/armario,
            - y tiene profundidad mayor que un mueble alto típico.
        ● Los muebles altos pueden llegar al techo y siguen siendo muebles altos
        si su estructura NO inicia en el piso.


        ──────────────────────────────────────────────
        FORMATO DE SALIDA OBLIGATORIO (JSON VÁLIDO)
        ──────────────────────────────────────────────

        Devuelve SIEMPRE un JSON válido con esta estructura EXACTA:

        {{
        "mensaje": "...",
        "mueble_tipo": "...",
        "componentes": [
            {{
            "nombre": "...",
            "tipo": "mueble_alto | mueble_bajo | closet | estructural",
            "cantidad": 1,
            "detalle": {{
                "puertas": ...,
                "cajones": ...,
                "entrepanos": ...,
                "relacionado_con": "..."
            }}
            }}
        ],
        "configuracion": "...",
        "comentarios": "...",
        "viabilidad": {{
            "porcentaje": 0-100,
            "razon": "..."
        }}
        }}

        ──────────────────────────────────────────────
        RESTRICCIONES:
        ──────────────────────────────────────────────
        - No agregues texto fuera del JSON.
        - No inventes módulos que no existan.
        - No clasifiques electrodomésticos como muebles.
        - Si algo no tiene puertas ni cajones → es estructural.
        - Si el plano es confuso, explica la duda en “viabilidad.razon”.
        - Sigue SIEMPRE esta taxonomía (no inventes categorías nuevas).
        - El apartado de 'mensaje' es para hablar con el usuario con el que interactuas.
        este apartado te permitira responder preguntas del mueble, enviar tu mensaje o en resumen, conversar con el usuario.
        - En caso de que hayan preguntas no es necesario diligenciar los campos de 'mueble_tipo', 'componentes', 'configuracion', 'comentarios' o 'viabilidad'
        si no influye o se requiere en el mensaje, entonces deja estos campos vacios segun su tipo de datos.

        Eres extremadamente riguroso, preciso y 100% coherente.
        Tu objetivo es reconstruir el mueble EXACTAMENTE como aparece en los planos.
    """

    model = OPENAI_MODELS["GPT-5 mini"]

    print(model)

    with open(r"C:\Users\autom\Desktop\CARPINTERIA\STAR GPT\Despiezador IA\output\Mueble TV\Mueble TV_piezas.json", "r", encoding="utf-8") as f:
        texto_out = f.read()

    print(texto_out)

    tokens_in = contar_tokens(text, modelo=model["nombre"])

    print(tokens_in)

    tokens_out = contar_tokens(texto_out, modelo=model["nombre"])

    print(tokens_out)

    value = calcular_costo(tokens_in, tokens_out, model["precio_entrada"], model["precio_salida"])

    print(f"El costo es: {value}, para in: {tokens_in} | out: {tokens_out}")