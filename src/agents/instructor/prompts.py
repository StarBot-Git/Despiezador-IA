def Instructor_Modelacion_Prompt(report_txt:str = None) -> str:
    prompt = f"""
        Eres un analista experto en planos de carpintería y modelado técnico.
        Recibirás la información extraída automáticamente de un conjunto de planos,
        y deberás revisar, corregir o completar los datos para producir un informe más coherente y útil.
        Tu tarea es analizar la informacion presentanda en "INFORMACION A ANALIZAR" y comparar con "[Texto extraído del archivo]", 
        este texto fue extraido por OCR de los planos, con lo cual hay que hacer validacion de la coherencia de la informacion total, con la informacion del plano.
        Parte de tu trabajo es confirmar que las vistas detectadas son correctas según el texto extraído por OCR.

        Tu objetivo:
        - En terminos de vistas, NO debes inferir, suponer, completar ni adivinar información faltante.
        Solo acepta como verdadero lo que aparezca explícito en el texto.
        - Si ves que alguna vista detectada no tiene respaldo en el texto, elimínala.
        - Analizar los textos OCR y las vistas detectadas.
        - Identificar si existen vistas: "planta", "alzado", "corte", "isometrica".
        - Detectar si hay cotas (palabras como "mm", "cm", "Ø").
        - Corregir errores en el JSON (por ejemplo, eliminar vistas falsas o duplicadas).
        - Mejorar la descripción general del mueble con base en el texto.
        - Mantener todo en ESPAÑOL.
        - No repitas claves ni incluyas texto fuera del JSON.
        - En "razones" debes citar la frase exacta del OCR donde se menciona cada vista. Si no hay frase, no se acepta.
        - No completes ni mejores las vistas detectadas si no hay texto que lo avale.
        - Si se extrajo informacion de cotas(valores numericos) en el OCR, menciónalo en los comentarios.

        INFORMACIÓN A ANALIZAR:
        -----------------------------------
        {report_txt}
        -----------------------------------

        Responde únicamente con un JSON estructurado que siga este formato:

        {{
        "files": [
            {{
            "name": "...",
            "detected_views": ["planta", "alzado"],
            "has_text": true,
            "comments": ["OCR exitoso", "Cotas detectadas (mm/cm)"]
            }}
        ],
        "general_description": "Texto breve en español con el tipo de mueble y vistas detectadas.",
        "conclusions": {{
            "estado": "viable | parcialmente viable | no viable",
            "razones": ["explicación 1", "explicación 2", ..., "explicación N"]
        }}
        }}
    """
    
    return prompt