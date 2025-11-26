from __future__ import annotations
import json
from pathlib import Path
from types import SimpleNamespace

# ====== IMPORTACIONES PROPIAS ======
from core.base_agent import BaseAgent
from core.config import OUTPUT_DIR
from agents.parametrizador.prompts import System_Prompt, Module_Prompt, USER_PROMPT
from agents.parametrizador.types import Modules_Description, ModuleParametrizationResult

class ParametrizadorModulos(BaseAgent):
    #SG_MODEL = "o4-mini"             # Modelo base
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

        self.text_format = Modules_Description

        self.init_state = False

        #______________________________________

    """
        Json_To_Message(self, data):
        Convierte un diccionario con información analizada del mueble en un mensaje formateado en texto para mostrar al usuario.  
        Incluye mensaje de IA, tipo de mueble, componentes, comentarios y viabilidad, pero solo si existen en el JSON.

            -self | objeto: Referencia a la instancia de la clase donde está definida la función.
            -data | dict: Diccionario con la información del análisis (mensaje, tipo, componentes, comentarios y viabilidad).
    """
    def Json_To_Message(self, data: dict) -> str:
        """
        Convierte a texto:
        - un JSON completo del Parametrizador (parametrizacion: [...])
        - un JSON de un solo módulo
        """

        # ---------------------------------------------------------------------
        # 🟦 CASO 1: JSON COMPLETO DEL PARAMETRIZADOR
        # ---------------------------------------------------------------------
        if isinstance(data, dict) and "parametrizacion" in data:
            mensajes = []
            for module in data["parametrizacion"]:
                mensajes.append(self.Json_To_Message(module))

            # Unir todos los módulos como texto independiente
            return "\n\n---\n\n".join(mensajes)

        # ---------------------------------------------------------------------
        # 🟧 CASO 2: JSON INDIVIDUAL DE UN MÓDULO
        # ---------------------------------------------------------------------

        name = data.get("name", "")
        type_component = data.get("type", "")
        global_pos = data.get("global_position", "")

        dimensions = data.get("dimensions", {})
        structure = data.get("structure", {})
        sub_modules = data.get("sub_modules", [])
        pieces = data.get("pieces", [])
        assumptions = data.get("assumptions", [])
        viability = data.get("viability", {})

        msg = []

        # ------ Nombre ------
        if name:
            msg.append(f"## 🗂️ **Módulo: {name}**\n")

        # ------ Tipo ------
        if type_component:
            msg.append(f"**Tipo:** {type_component.replace('_', ' ').title()}")

        # ------ Posición ------
        if global_pos:
            msg.append(f"**Posición en el conjunto:** {global_pos}\n")

        # ------ Dimensiones ------
        if dimensions:
            msg.append("### 📐 **Dimensiones del módulo**")
            h = dimensions.get("height")
            w = dimensions.get("width")
            d = dimensions.get("depth")
            u = dimensions.get("unit", "mm")

            if h is not None: msg.append(f"- **Alto:** {h}{u}")
            if w is not None: msg.append(f"- **Ancho:** {w}{u}")
            if d is not None: msg.append(f"- **Profundidad:** {d}{u}")

        # ------ Estructura ------
        if structure:
            msg.append("\n### 🧱 **Estructura general**")
            msg.append(f"- Puertas: **{structure.get('doors', 0)}**")
            msg.append(f"- Cajones: **{structure.get('drawers', 0)}**")
            msg.append(f"- Repisas: **{structure.get('shelves', 0)}**")
            msg.append(f"- Cavidades internas: **{structure.get('cavities', 0)}**")

        # ------ Sub-módulos ------
        if sub_modules:
            msg.append("\n### 🗂️ **Sub-módulos internos**")
            for sm in sub_modules:
                msg.append(f"- **{sm.get('name', '').title()}** ({sm.get('type', '')})")
                msg.append(f"  - Ubicación: *{sm.get('relative_position', '-') }*")
                msg.append(f"  - Especificación: *{sm.get('specifications', '-') }*")

                dim = sm.get("dimensions", {})
                hs = dim.get("height")
                ws = dim.get("width")
                ds = dim.get("depth")
                us = dim.get("unit", "mm")

                if hs and ws and ds:
                    msg.append(f"  - Dimensiones: {hs}×{ws}×{ds}{us}\n")
                else:
                    msg.append("  - Dimensiones incompletas\n")

        # ------ Piezas ------
        if pieces:
            msg.append("\n### 🔩 **Piezas del módulo**")
            for p in pieces:
                msg.append(
                    f"- **{p.get('quantity', 1)} × {p.get('name', '').title()}** "
                    f"({p.get('role', '')}) — "
                    f"{p.get('height')}×{p.get('width')}×{p.get('depth')}mm"
                )

        # ------ Suposiciones ------
        if assumptions:
            msg.append("\n### 🧠 **Suposiciones del análisis**")
            for a in assumptions:
                msg.append(f"- {a}")

        # ------ Viabilidad ------
        if viability:
            msg.append("\n### 📊 **Viabilidad**")
            msg.append(f"- **{viability.get('percentage', 0)}%** de confianza")
            reason = viability.get("reason")
            if reason:
                msg.append(f"- Motivo: *{reason}*")

            missing = viability.get("missing_data", [])
            if missing:
                msg.append("\n### ⚠️ **Datos faltantes**")
                for m in missing:
                    msg.append(f"- {m}")

        # Si no se generó nada
        if not msg:
            return "⚠️ No se pudo generar información del módulo."
        
        response_txt = "\n".join(msg)

        if self.init_state == False:
            self.messages.append({"role": "assistant", "content": response_txt})

        return response_txt
    
        #_______________________________________________________________________________________________

    def Update_SingleModule(self, file_path: str, new_module_obj):
        """
        Reemplaza SOLO el módulo cuyo 'name' coincide con new_module_obj.name
        dentro del archivo JSON.
        """

        new_module = new_module_obj.dict()
        target_name = new_module.get("name")

        if not target_name:
            print("[ERROR] El módulo no tiene campo 'name'")
            return

        # ----------------------------------------------------
        # 1. Leer JSON actual
        # ----------------------------------------------------
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("[WARN] JSON no existe, creando uno nuevo...")
            data = {"parametrizacion": [], "tokens": {}}

        modules = data.get("parametrizacion", [])

        # ----------------------------------------------------
        # 2. Buscar y reemplazar el módulo
        # ----------------------------------------------------
        replaced = False
        for idx, module in enumerate(modules):
            if module.get("name") == target_name:
                modules[idx] = new_module
                replaced = True
                print(f"[OK] Módulo actualizado: {target_name}")
                break

        # Si no existía antes → agregarlo
        if not replaced:
            print(f"[INFO] El módulo '{target_name}' no existía. Añadiéndolo.")
            modules.append(new_module)

        # ----------------------------------------------------
        # 3. Guardar el JSON reparado y actualizado
        # ----------------------------------------------------
        data["parametrizacion"] = modules

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"[OK] JSON guardado en {file_path}")

    def Run_Loop(self, furniture_name:str=None, progress_cb=None):
        json_path = str(OUTPUT_DIR / furniture_name / f"{furniture_name}_piezas.json")

        #print(json_path)

        # ------------------------------------------------------------------
        # 1. Leer el JSON del Analista
        # ------------------------------------------------------------------
        json_path = Path(json_path)

        if not json_path.exists():
            raise FileNotFoundError(f"No existe el archivo JSON: {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        components = data.get("components", [])

        if not components:
            print("[Parametrizador] No se encontraron módulos.")
            return None, None
        
        #print(components)

        # ------------------------------------------------------------------
        # Variables acumuladoras
        # ------------------------------------------------------------------
        results = []  # guarda todos los output_parsed (JSON del modelo)

        total_input_tokens = 0
        total_output_tokens = 0
        total_tokens = 0
        indx = 1

        #input("Presiona Enter para continuar...")
        
        # ------------------------------------------------------------------
        # 2. Extraer lista de módulos
        # ------------------------------------------------------------------
        for comp in components:
            if progress_cb:
                progress_cb(f"✍️ Analizando {indx} de {len(components)} modulos...")
            # Reset del historial para que cada módulo sea independiente
            # input("Presiona Enter para continuar...")
            self.Reset_History()
            self.content = []
            self.Add_Files()

            # ------------------------------------------------------------------
            # 3. Construir PROMPT por módulo
            # ------------------------------------------------------------------
            type_furniture = data.get("type_furniture", "desconocido")
            configuration = data.get("configuration", "")
            name = comp.get("name", "sin_nombre")
            type_component = comp.get("type_component", "desconocido")
            quantity = comp.get("quantity", 1)
            detail = comp.get("detail", {})

            # Puedes refinar este prompt luego, pero funcional está bien
            prompt = f"""
            Eres el PARAMETRIZADOR OFICIAL de Star GPT WoodWork.

            Tu tarea es analizar UN SOLO módulo del mueble y devolver su parametrización técnica en JSON puntual, precisa y utilizable para fabricación.

            === CONTEXTO GENERAL DEL MUEBLE ===
            Tipo de mueble: {type_furniture}
            Configuración general: {configuration}

            === MÓDULO A PARAMETRIZAR ===
            Nombre: {name}
            Tipo de componente: {type_component}
            Cantidad: {quantity}

            === DETALLES DEL MÓDULO ===
            {json.dumps(detail, ensure_ascii=False, indent=2)}

            === INSTRUCCIONES ===
            1. Analiza el módulo teniendo en cuenta el tipo de mueble y su configuración.
            2. Si el módulo es parte de una puerta, cajón, repisa o estructura, ajusta la parametrización según reglas habituales de carpintería.
            3. No inventes medidas si no existen, pero sí puedes sugerirlas si lo consideras necesario.
            4. Devuelve SOLO un JSON con la parametrización final del módulo.

            """

            #print(prompt)

            # ------------------------------------------------------------------
            # 4. Llamar al modelo con run()
            # ------------------------------------------------------------------
            parsed, usage = self.Run(prompt=prompt)

            # Añadir resultado al array final
            results.append(parsed.model_dump())

            # Acumular tokens
            total_input_tokens += usage.input_tokens
            total_output_tokens += usage.output_tokens
            total_tokens += usage.total_tokens

            print("[Acabo parametrizacion...]\n")
            indx += 1

            #print(json.dumps(parsed.model_dump(), indent=2, ensure_ascii=False))

        # ------------------------------------------------------------------
        # JSON Final
        # ------------------------------------------------------------------
        # 1) Crear parsed_total como Pydantic Model
        parsed_total = ModuleParametrizationResult(
            parametrizacion=results,
            tokens={
                "input": total_input_tokens,
                "output": total_output_tokens,
                "total": total_tokens
            }
        )

        # 2) Crear usage_total compatible con el UI
        usage_total = SimpleNamespace(
            input_tokens=total_input_tokens,
            output_tokens=total_output_tokens,
            total_tokens=total_tokens
        )

        # 3) Retornar EXACTAMENTE como un agente normal
        return parsed_total, usage_total
