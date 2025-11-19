from openai import OpenAI
from pydantic import BaseModel
from pathlib import Path
import os
import json

client = OpenAI()

#_______________________________________________________________
# INSTRUCTOR DE MODELACION

class FileResult(BaseModel):
    name: str
    detected_views: list[str]
    has_text: bool
    comments: list[str]

class Conclusions(BaseModel):
    estado: str
    razones: list[str]

class ReportAIResult(BaseModel):
    files: list[FileResult]
    general_description: str
    conclusions: Conclusions

#_______________________________________________________________
# ANALISTA DE PIEZAS

class Viability(BaseModel):
    percentage: int
    reason: str

class Detail(BaseModel):
    doors: int
    drawers: int
    shelves: int
    related_to: str

class Components(BaseModel):
    name: str
    type_component: str
    quantity: int
    detail: Detail

class Disassemble(BaseModel):
    type_furniture: str
    components: list[Components]
    configuration: str
    comments: str
    viability: Viability

#_______________________________________________________________
# Metodos de OpenAI

def send_request(model, input, model_name, temperature):

    text_format = None

    if model_name == "Instructor_Modelacion":
        text_format = ReportAIResult
    elif model_name == "Analista_Piezas" or "Supervisor_Piezas":
        text_format = Disassemble

    print(f"[IA] Temperature: {temperature}")
    return client.responses.parse(model=model, input=input, text_format=text_format)

def upload_file(local_FileName:str, path:str = None, purpose:str="user_data"):
    base_dir = Path(__file__).resolve().parents[2] # Ruta del proyecto → /DESPIEZADOR IA/
    ID_REGISTER = base_dir / "assets" / "file_ids.json"
    
    if path:
        data = {}
        if os.path.exists(ID_REGISTER):
            with open(ID_REGISTER, "r", encoding="utf-8") as file:
                data = json.load(file)

        with open(path, "rb") as file_OpenAI:
            file_id = client.files.create(file=file_OpenAI, purpose=purpose).id

        data[local_FileName] = file_id

        with open(ID_REGISTER, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"[Archivos OpenAI] Se creo el ID de {local_FileName}:{file_id}")

        return file_id
    
    return None
    
def load_file(local_FileName:str):
    base_dir = Path(__file__).resolve().parents[2] # Ruta del proyecto → /DESPIEZADOR IA/
    ID_REGISTER = base_dir / "assets" / "file_ids.json"

    if not os.path.exists(ID_REGISTER):
        return None
    
    with open(ID_REGISTER, "r", encoding="utf-8") as file:
        data = json.load(file)

    if data.get(local_FileName):
        print(f"[Archivos OpenAI] Se recupero el ID de {local_FileName}:{data.get(local_FileName)}")

    return data.get(local_FileName)