from __future__ import annotations

# ====== IMPORTACIONES PROPIAS ======
from core.base_agent import BaseAgent
from agents.analista.prompts import System_Prompt, USER_PROMPT
from agents.analista.types import Disassemble

class Analista_Piezas(BaseAgent):
    SG_MODEL = "gpt-5-mini"             # Modelo base
    SG_RESPONSE_FORMAT = "json_object"  # Formato JSON
    SG_TEMPERATURE = 0.5                # Temperatura flexible
    SG_USER_PROMPT = USER_PROMPT        # Prompt recomendado

    def __init__(self, ai_client):
        #_____________________________________
        
        super().__init__(
            ai_client=ai_client,
            system_prompt=System_Prompt(),
            model=self.SG_MODEL,
            temperature=self.SG_TEMPERATURE
        )

        self.text_format = Disassemble

        #______________________________________

    """
        Json_To_Message(self, data):
        Convierte un diccionario con información analizada del mueble en un mensaje formateado en texto para mostrar al usuario.  
        Incluye mensaje de IA, tipo de mueble, componentes, comentarios y viabilidad, pero solo si existen en el JSON.

            -self | objeto: Referencia a la instancia de la clase donde está definida la función.
            -data | dict: Diccionario con la información del análisis (mensaje, tipo, componentes, comentarios y viabilidad).
    """
    def Json_To_Message(self, data: dict) -> str:
        #_______________________________________________________________________________________________
        #   Extraccion de datos | Creacion de variables

        msg_IA = data.get("message", "")
        tipo = data.get("type_furniture", "")
        components = data.get("components", [])
        viability = data.get("viability", {})
        viability_pct = viability.get("percentage", None)
        comments = data.get("comments", "")

        #_______________________________________________________________________________________________
        #   Creacion de mensaje

        msg = []

        # ------ Encabezado ------
        if msg_IA:
            msg.append(f"{msg_IA}\n")

        # ------ Agregar | Tipo de mueble ------
        if tipo and tipo != "mueble desconocido":
            msg.append(f"🔍 **Análisis del mueble identificado: {tipo.replace('_', ' ').title()}**\n")

        # ------ Enlistar | Componentes ------
        if components:
            msg.append("### 🧩 **Componentes detectados**")

            for comp in components:
                nombre = comp.get("name", "").replace("_", " ")
                tipo_comp = comp.get("type_component", "")
                cantidad = comp.get("quantity", 1)

                det = comp.get("detail", {})
                related = det.get("related_to", "-")

                msg.append(
                    f"- **{cantidad} × {nombre.title()}** "
                    f"({tipo_comp})\n"
                    f"  - Relación: *{related}*"
                )

        # ------ Agregar | Comentarios generales ------
        if comments:
            msg.append("\n### 📝 **Comentarios generales**")
            msg.append(comments)

        # ------ Agregar | Viabilidad ------
        if viability_pct is not None and viability_pct != 0:
            msg.append("\n### 📊 **Viabilidad estimada del análisis**")
            msg.append(f"- **{viability_pct}%** de claridad estructural general.")

        # ------ Error | Sin datos que mostrar ------
        if not msg:
            return "⚠️ No se pudo generar el análisis. Por favor, intenta nuevamente."

        return "\n".join(msg)
    
        #_______________________________________________________________________________________________