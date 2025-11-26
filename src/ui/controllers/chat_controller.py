import json

from PySide6.QtCore import QTimer

from ui.components.message_bubble import MessageBubble
from ui.workers.ai_worker import AIWorker

class ChatController:
    def __init__(self, main_window = None):
        self.main_window = main_window
        self.chat_area = main_window.chat_area

    """
        Add_Message():
    """
    def Add_Message(self, text, role="assistant"):
        bubble = MessageBubble(text, role)
        
        self.chat_area.layout.insertWidget(self.chat_area.layout.count() - 1, bubble)
        
        # Auto scroll al final (con delay para que se renderice el widget)
        QTimer.singleShot(10, lambda: self.chat_area.scroll.verticalScrollBar().setValue(
            self.chat_area.scroll.verticalScrollBar().maximum()
        ))

    def Remove_LastMessage(self):
        """
        Remueve el último mensaje del chat.
        Útil para eliminar mensajes temporales como "Analizando..."
        """
        if self.chat_area.layout.count() > 1:  # Debe haber al menos 1 mensaje + stretch
            # El último item es el stretch, el penúltimo es el mensaje
            last_msg_index = self.chat_area.layout.count() - 2
            last_item = self.chat_area.layout.itemAt(last_msg_index)
            
            if last_item and last_item.widget():
                widget = last_item.widget()
                self.chat_area.layout.removeWidget(widget)
                widget.deleteLater()

    def Save_OutputJSON(self, response_obj):
        # ----------------------------------------------------
        # 1. Determinar tipo de archivo (piezas/modulos)
        # ----------------------------------------------------
        keyword_file = "none"
        agent_name = self.main_window.agent_IA.__class__.__name__

        if agent_name == "ParametrizadorModulos":
            keyword_file = "modulos"
        elif agent_name == "Analista_Piezas":
            keyword_file = "piezas"

        file_JSON = f"{self.main_window.output_dir}\\{self.main_window.furniture_name}_{keyword_file}.json"

        # ----------------------------------------------------
        # 2. SI ES UN MODULO PARAMETRIZADO → actualizar solo 1 módulo
        # ----------------------------------------------------
        if agent_name == "ParametrizadorModulos":
            if self.main_window.agent_IA.init_state == True:
                self.main_window.agent_IA.Update_SingleModule(file_JSON, response_obj)
                return
            else:
                self.main_window.agent_IA.init_state = True
        
        # ----------------------------------------------------
        # 3. SI NO ES PARAMETRIZADOR → guardar JSON normal
        # ----------------------------------------------------
        with open(file_JSON, "w", encoding="utf-8") as f:
            json.dump(response_obj.dict(), f, indent=4, ensure_ascii=False)

    def Handle_SendMessage(self):
        """Método actualizado con Threading"""
        text = self.main_window.input_field.toPlainText().strip()

        if not text:
            return

        # Deshabilitar el botón mientras procesa
        self.main_window.send_button.setEnabled(False)
        self.main_window.send_button.setText("  Procesando...")
        
        # Agregar mensaje del usuario
        self.Add_Message(text, role="user")
        
        # Limpiar el campo de entrada
        self.main_window.input_field.clear()
        
        # Agregar mensaje temporal "IA escribiendo..."
        self.Add_Message("✍️ Analizando...", role="assistant")

        # Crear y configurar el worker thread
        self.ai_worker = AIWorker(self.main_window.agent_IA, text, self.main_window.furniture_name)
        
        # Conectar las señales
        self.ai_worker.finished.connect(self.On_IA_Response)
        self.ai_worker.error.connect(self.On_IA_Error)
        self.ai_worker.progress.connect(self.On_IA_Progress)
        
        # Iniciar el thread (no bloquea la interfaz)
        self.ai_worker.start()

    def On_IA_Response(self, output_obj, response_usage):
        # Remover el mensaje temporal "Analizando..."
        self.Remove_LastMessage()
        
        # Convertir respuesta a texto legible
        output_msg = self.main_window.agent_IA.Json_To_Message(output_obj.dict())
        
        # Agregar respuesta de la IA
        self.Add_Message(output_msg, role="assistant")
        
        # Guardar el JSON
        self.Save_OutputJSON(output_obj)

        tokens_in, tokens_out = response_usage.input_tokens, response_usage.output_tokens

        self.main_window.chat_topbar.controller.Update_Tokens(response_usage.total_tokens)
        self.main_window.chat_topbar.controller.Update_Cost(tokens_in, tokens_out)

        # self.tokens += int(tokens)
        # self.tokens_price += float(price)

        # print(self.tokens_price)

        # self.chat_topbar.card_tokens.lbl_value.setText(f"{self.tokens:,}".replace(",", " "))
        # self.chat_topbar.card_tokens_price.lbl_value.setText( str( round(self.tokens_price,3) ) )
        
        # Rehabilitar el botón
        self.main_window.send_button.setEnabled(True)
        self.main_window.send_button.setText("  Enviar")
        
        print(f"[{self.main_window.agent_IA.__class__.__name__}] Respuesta recibida exitosamente")

    def On_IA_Error(self, error_msg):
        """Se ejecuta si hay un error en el worker"""
        
        # Remover el mensaje temporal
        self.Remove_LastMessage()
        
        # Mostrar error
        self.Add_Message(f"❌ Error: {error_msg}", role="assistant")
        
        # Rehabilitar el botón
        self.main_window.send_button.setEnabled(True)
        self.main_window.send_button.setText("  Enviar")
        
        print(f"[ERROR] {error_msg}")

    def On_IA_Progress(self, msg):
        self.Remove_LastMessage()

        self.Add_Message(msg, role="assistant")
