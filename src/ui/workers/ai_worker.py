from PySide6.QtCore import QThread, Signal

class AIWorker(QThread):
    """
    Worker thread que ejecuta agent_IA.run() en segundo plano
    para no bloquear la interfaz gráfica.
    """
    # Señales para comunicarse con la interfaz principal
    finished = Signal(object, float, int)  # Envía output_obj cuando termina
    error = Signal(str)        # Envía mensaje de error si falla
    
    def __init__(self, agent_IA, prompt):
        super().__init__()
        self.agent_IA = agent_IA
        self.prompt = prompt
    
    def run(self):
        """Este método se ejecuta en el hilo separado"""
        try:
            # Aquí va la llamada que bloquea

            

            output_obj, price, tokens = self.agent_IA.run(prompt=self.prompt)

            print("HOLA 1")
            
            # Emitir señal con el resultado
            self.finished.emit(output_obj, price, tokens)
            
        except Exception as e:
            # Si algo sale mal, emitir error
            self.error.emit(str(e))