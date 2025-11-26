from PySide6.QtCore import QThread, Signal

class AIWorker(QThread):
    finished = Signal(object, object)  # Envía output_obj cuando termina
    error = Signal(str)        # Envía mensaje de error si falla
    progress = Signal(str)
    
    def __init__(self, agent_IA, prompt, furniture_name):
        super().__init__()
        self.agent_IA = agent_IA
        self.prompt = prompt
        self.furniture_name = furniture_name
    
    def run(self):
        """Este método se ejecuta en el hilo separado"""
        try:
            # Aquí va la llamada que bloquea

            # print(self.agent_IA.__class__.__name__)
            # input("Presiona Enter para continuar...")

            if self.agent_IA.__class__.__name__ == "ParametrizadorModulos":
                if self.agent_IA.init_state == False:
                    print("PRIMER RESPONSE")
                    output_obj, response_usage = self.agent_IA.Run_Loop(self.furniture_name, progress_cb = lambda msg:self.progress.emit(msg))
                else:
                    print("CHAT ACTIVO")
                    output_obj, response_usage = self.agent_IA.Run(prompt=self.prompt)
            else:
                output_obj, response_usage = self.agent_IA.Run(prompt=self.prompt)
            
            # Emitir señal con el resultado
            self.finished.emit(output_obj, response_usage)
            
        except Exception as e:
            # Si algo sale mal, emitir error
            self.error.emit(str(e))