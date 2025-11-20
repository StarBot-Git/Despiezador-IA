from agents.ai_client import send_request
import json

class BaseAgent:
    def __init__(self, system_prompt, model, temperature, default_tools, files):
        self.model = model
        self.system_prompt = system_prompt
        self.default_tools = default_tools or []
        self.messages = [{"role": "system", "content": system_prompt}]
        self.temperature = temperature
        self.files = files

    def run(self, prompt):

        print(f"[{self.__class__.__name__}] Hizo su peticion a OpenAI")

        model_name = self.__class__.__name__

        content = []
        #content.append({"type":"input_text", "text":prompt, "variables":variables})
        content.append({"type":"input_text", "text":prompt})

        if self.files:
            for file_id, file_type in self.files.items():
                input_type = "input_file" if file_type == 'pdf' else "input_image"
                content.append({"type": input_type, "file_id": file_id})

        self.messages.append({"role":"user", "content":content})

        print(self.messages)

        response = send_request(model=self.model, input = self.messages, model_name=model_name, temperature=self.temperature)

        # --- ASSISTANT CONTENT | Respuesta completa de la IA ---
        # output_assistant_msg = json.dumps(response.model_dump(), ensure_ascii=False, indent=2)
        # self.messages.append({"role":"assistant", "content":output_assistant_msg})

        output = response.output_parsed

        output_assistant_msg = json.dumps(output.dict(), ensure_ascii=False, indent=2)
        self.messages.append({"role":"assistant", "content":output_assistant_msg})

        return output
    
    def json_to_message(self, data: dict) -> str:
        """
        Convierte la estructura JSON del mueble en un mensaje legible estilo IA.
        Ignora 'configuration' y 'viability.reason'.
        """

        tipo = data.get("type_furniture", "mueble desconocido")
        components = data.get("components", [])
        viability = data.get("viability", {})
        viability_pct = viability.get("percentage", None)
        comments = data.get("comments", "")

        # ---- Encabezado ----
        msg = []
        msg.append(f"🔍 **Análisis del mueble identificado: {tipo.replace('_', ' ').title()}**\n")

        # ---- Componentes ----
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
        if viability_pct is not None:
            msg.append("\n### 📊 **Viabilidad estimada del análisis**")
            msg.append(f"- **{viability_pct}%** de claridad estructural general.")

        return "\n".join(msg)
