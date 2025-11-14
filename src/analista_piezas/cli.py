from __future__ import annotations
from pathlib import Path
import os
import json

# === IMPORTACIONES PROPIAS ===
from utils.paths import Normalize_Path, Ensure_OutputsRoot
from utils.scanner import Scan_InputFolder
from agents.ai_client import load_file, upload_file

from agents.sg_analista_piezas import Analista_Piezas


def Run_Analyst(input_dir:str, output_root:str, report_dir:str, furniture_name:str):
    #__________________________________________________________________________
    #  Preparacion de rutas

    input_dir = Normalize_Path(input_dir)           # utils.paths | Normaliza ruta
    outputs_root = Ensure_OutputsRoot(output_root)  # utils.paths | Asegura existencia de la ruta

    #__________________________________________________________________________
    #  Recuperacion del reporte de [Instructor de Modelacion]

    # with open(report_dir, "r", encoding="utf-8") as file:
    #     report = file.read()

    #__________________________________________________________________________
    #  Preparacion de archivos para IA

    paths = Scan_InputFolder(input_dir)

    file_IDs = []

    for p in paths:
        local_filename = f"{furniture_name}-{os.path.splitext(os.path.basename(p))[0]}"

        file_id = load_file(local_filename)

        if file_id == None:
            file_id = upload_file(local_FileName=local_filename, path=p)

        file_IDs.append(file_id)

    print(file_IDs)

    #__________________________________________________________________________
    #  MODELO IA | Analista de Piezas

    agent_IA = Analista_Piezas()
    disassemble_obj = agent_IA.Disassemble(files=file_IDs)

    file_JSON = f"{output_root}\\{furniture_name}_piezas.json"

    print(disassemble_obj)

    with open(file_JSON, "w", encoding="utf-8") as f:
        json.dump(disassemble_obj.dict(), f, indent=4, ensure_ascii=False)