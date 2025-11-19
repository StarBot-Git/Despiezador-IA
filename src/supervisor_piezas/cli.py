from __future__ import annotations
from pathlib import Path
import os
import json

# === IMPORTACIONES PROPIAS ===
from utils.paths import Normalize_Path, Ensure_OutputsRoot
from utils.scanner import Scan_InputFolder
from agents.ai_client import load_file, upload_file

from agents.sg_supervisor_piezas import Supervisor_Piezas

def Run_Supervisor(input_dir:str, output_root:str, file_pieces_JSON:str, furniture_name:str, files=None):
    #__________________________________________________________________________
    #  Preparacion de rutas

    input_dir = Normalize_Path(input_dir)           # utils.paths | Normaliza ruta
    output_root = Ensure_OutputsRoot(output_root)  # utils.paths | Asegura existencia de la ruta

    #__________________________________________________________________________
    #  Recuperacion del reporte de [Instructor de Modelacion]

    with open(file_pieces_JSON, "r", encoding="utf-8") as file:
        pieces_JSON = file.read()

    #__________________________________________________________________________
    #  Preparacion de archivos para IA

    paths = Scan_InputFolder(input_dir)

    file_data = {}

    for p in paths:
        local_filename = f"{furniture_name}-{os.path.splitext(os.path.basename(p))[0]}"
        
        file_id = load_file(local_filename)
        
        if file_id == None:
            file_id = upload_file(local_FileName=local_filename, path=p)
        
        # Obtener la extensión y clasificarla
        extension = os.path.splitext(p)[1].lower()  # .jpg, .png, .pdf, etc.
        
        if extension == '.pdf':
            file_type = 'pdf'
        elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
            file_type = 'img'
        else:
            file_type = 'other'  # Por si acaso hay otros tipos
        
        file_data[file_id] = file_type

    print(file_data)

    files = file_data

    print(files)

    #__________________________________________________________________________
    #  MODELO IA | Supervisor de Piezas

    agent_IA = Supervisor_Piezas()
    disassemble_obj = agent_IA.Disassemble_Corrected(files, pieces_JSON)

    file_JSON = f"{output_root}\\{furniture_name}_piezas_CORREGIDAS.json"

    #print(disassemble_obj)

    with open(file_JSON, "w", encoding="utf-8") as f:
        json.dump(disassemble_obj.dict(), f, indent=4, ensure_ascii=False)