from PySide6.QtCore import QThread, Signal

class AIWorker(QThread):
    finished = Signal(object, object)  # Envía output_obj cuando termina
    error = Signal(str)        # Envía mensaje de error si falla
    
    def __init__(self, agent_IA, prompt):
        super().__init__()
        self.agent_IA = agent_IA
        self.prompt = prompt
    
    def run(self):
        """Este método se ejecuta en el hilo separado"""
        try:
            # Aquí va la llamada que bloquea

            output_obj, response_usage = self.agent_IA.Run(prompt=self.prompt)
            
            # Emitir señal con el resultado
            self.finished.emit(output_obj, response_usage)
            
        except Exception as e:
            # Si algo sale mal, emitir error
            self.error.emit(str(e))