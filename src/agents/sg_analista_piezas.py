from __future__ import annotations
import json
from typing import Any
from agents.base_agent import BaseAgent
from config.prompts import Analista_Piezas_Prompt

class Analista_Piezas(BaseAgent):
    #SG_MODEL = "gpt-4.1-nano"
    SG_MODEL = "gpt-5-mini"
    SG_RESPONSE_FORMAT = "json_object"
    SG_TEMPERATURE = 0.5
    SG_USER_PROMPT = f"""Analiza los planos adjuntos y genera el JSON del mueble según las reglas del sistema. Incluye los componentes y su clasificación exacta según los dibujos. No agregues texto fuera del JSON."""

    def __init__(self, files = None):
        super().__init__(
            system_prompt=Analista_Piezas_Prompt(), 
            model=self.SG_MODEL,
            default_tools=[],
            temperature=self.SG_TEMPERATURE,
            files=files
        )

    def json_to_message(self, data: dict) -> str:
        """
        Convierte la estructura JSON del mueble en un mensaje legible estilo IA.
        Ignora 'configuration' y 'viability.reason'.
        """
        msg_IA = data.get("message", "")
        tipo = data.get("type_furniture", "")
        components = data.get("components", [])
        viability = data.get("viability", {})
        viability_pct = viability.get("percentage", None)
        comments = data.get("comments", "")

        # ---- Encabezado ----
        msg = []

        # Solo agregar mensaje de IA si existe
        if msg_IA:
            msg.append(f"{msg_IA}\n")

        # Solo agregar tipo si existe y no es el default
        if tipo and tipo != "mueble desconocido":
            msg.append(f"🔍 **Análisis del mueble identificado: {tipo.replace('_', ' ').title()}**\n")

        # ---- Componentes ----
        # Solo mostrar sección si hay componentes
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

        # ---- Comentarios generales ----
        if comments:
            msg.append("\n### 📝 **Comentarios generales**")
            msg.append(comments)

        # ---- Viabilidad ----
        if viability_pct is not None and viability_pct is not 0:
            msg.append("\n### 📊 **Viabilidad estimada del análisis**")
            msg.append(f"- **{viability_pct}%** de claridad estructural general.")

        # Si no hay nada que mostrar, retornar mensaje por defecto
        if not msg:
            return "⚠️ No se pudo generar el análisis. Por favor, intenta nuevamente."

        return "\n".join(msg)


    def Disassemble(self, prompt = None):
        # --- Prompt ---
        if prompt == None:
            prompt = self.SG_USER_PROMPT

        # --- Ejecutar agente ---
        print("[AI_Refiner] Enviando informe preliminar al modelo IA...")
        
        model_Output = self.run(prompt=prompt, files=self.files)

        return model_Output