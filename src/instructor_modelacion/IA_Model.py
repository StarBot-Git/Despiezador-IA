from __future__ import annotations
import json
from typing import Any
from openai import OpenAI
from instructor_modelacion.utils.types import Report, File_Analyzed

# --- Inicializa el cliente con tu API key ya configurada ---
client = OpenAI()  # Usa la variable de entorno OPENAI_API_KEY

# ==========================================================
# FUNCION PRINCIPAL
# ==========================================================

"""
    Report_With_AI():
    Envía el texto del reporte y los datos detectados a un modelo de IA (OpenAI)
    para que los analice, corrija y complete.
    Devuelve un nuevo objeto Report refinado.
"""
def Report_With_AI(report: Report, report_text: str) -> Report:
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
    {report_text}
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

    print("[AI_Refiner] Enviando informe preliminar al modelo IA...")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Eres un asistente técnico experto en análisis de planos."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        # Intento 1: formato moderno con JSON ya parseado
        try:
            refined_data = response.choices[0].message.parsed
        except AttributeError:
            # Intento 2: lectura tradicional de texto
            raw_text = response.choices[0].message.content or ""
            raw_text = raw_text.strip()
            if not raw_text:
                raise ValueError("Respuesta vacía del modelo IA.")
            refined_data = json.loads(raw_text)

        print("[ai_refiner] Respuesta IA recibida y procesada correctamente.")

    except Exception as e:
        print(f"[ai_refiner] Error al interpretar respuesta IA: {e}")
        # Para depurar, imprime la respuesta cruda si existe
        try:
            print(f"\n[ai_refiner] Respuesta cruda:\n{response}\n")
        except Exception:
            pass
        return report


    # ==========================================================
    # RECONSTRUIR EL NUEVO OBJETO REPORT
    # ==========================================================

    # Sobrescribe solo los campos que la IA corrigió
    for ai_file in refined_data.get("files", []):
        for original in report.files:
            if ai_file.get("name") == original.name:
                if "detected_views" in ai_file:
                    original.detected_views = ai_file["detected_views"]
                if "comments" in ai_file:
                    original.comments.extend(ai_file["comments"])
                if "has_text" in ai_file:
                    original.has_text = ai_file["has_text"]

    # Actualiza descripción general y conclusiones
    if "general_description" in refined_data:
        report.general_description = refined_data["general_description"]

    if "conclusions" in refined_data:
        report.conclusions = refined_data["conclusions"]

    return report