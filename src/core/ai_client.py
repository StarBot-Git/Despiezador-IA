from openai import OpenAI

class AIClient:
    def __init__(self):
        #_____________________________________

        self.client = OpenAI()  # Cliente OpenAI

        #_____________________________________

    """
        Send_Request(self, model, input, text_format, temperature):
        Envía una solicitud al cliente de IA para procesar un input y devuelve la respuesta ya parseada por el modelo.

            -self | objeto: Instancia actual que contiene el cliente de IA.
            -model | str: Nombre o identificador del modelo que procesará la solicitud.
            -input | List: Contenido que se envía al modelo (texto, lista de mensajes, etc.).
            -text_format | str | None: Formato opcional que indica cómo debe interpretarse el texto.
            -temperature | float: Valor que controla la variabilidad/creatividad de la respuesta del modelo.
    """
    def Send_Request(self, model, input, text_format=None, temperature=0.3):
        #_____________________________________________________________________________________
        
        return self.client.responses.parse(model=model, input=input, text_format=text_format)
    
        #_____________________________________________________________________________________