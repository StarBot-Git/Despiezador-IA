from __future__ import annotations
from pathlib import Path
from typing import List, Dict

# === IMPORTACIONES PROPIAS ===
from utils.paths import Normalize_Path, Ensure_OutputsRoot
from utils.types import File_Analyzed, Report
from utils.scanner import Scan_InputFolder, Guess_Type
from .analyzers.pdf_analyzer import PDF_Analyzer
from .analyzers.image_analyzer import Image_Analyzer
from .summarizer import Furniture_Description
from .reporter import Write_Outputs, now_iso, Report_To_Text
from agents.sg_instructor_modelacion import Instructor_Modelacion

VERSION_MODULO = "0.2.0"

"""
    Run_Instructor():
    Funcion de ejecucion del instructor de modelacion.

    - input_dir | Path: Ruta del mueble a analizar.
    - Outputs_root | Path: Ruta para salida de informes
"""
def Run_Instructor(input_dir: Path, outputs_root: Path):

    #__________________________________________________________________________
    #   Preparacion de rutas

    input_dir = Normalize_Path(input_dir)           # utils.paths | Normaliza ruta
    outputs_root = Ensure_OutputsRoot(outputs_root) # utils.paths | Asegura existencia de la ruta

    #__________________________________________________________________________
    #   Escaneo y analisis de archivos

    # --- Verificacion | archivo de entrada existente ---
    if not input_dir.exists():
        raise SystemExit(f"[error] No existe la ruta de entrada: {input_dir}")

    # --- Nombre del mueble actual ---
    furniture_name = input_dir.name
    print(f"[inicio] Proyecto: {furniture_name}")
    print(f"[inicio] Escaneando ruta: {input_dir}")

    # --- Obtener | Lista de archivos en la ruta de entrada ---
    paths = Scan_InputFolder(input_dir) # .scanner | Lista de paths

    analyzed: List[File_Analyzed] = [] # Var | Lista de archivos analizados 

    # --- Recorrido | Analisis individual de cada archivo ---
    for p in paths:
        t = Guess_Type(p) # .scanner | Tipo de archivo detectado

        # --- Inicializacion | Archivo analizado ---
        a = File_Analyzed(name=p.name, extension=p.suffix.lower(), path=str(p), type_detected=t)
        print(f"[analiza] {p.name} -> {t}")

        # --- Analisis | Segun tipo detectado ---
        if t == "pdf":
            # --- PDF_Analyzer | Analisis de metadatos del PDF ---
            meta = PDF_Analyzer(p)

            a.is_vector = meta.get("es_vectorial")
            a.pages = meta.get("paginas")
            a.has_text = meta.get("tiene_texto")
            a.detected_views = meta.get("vistas_detectadas", [])
            a.comments.extend(meta.get("observaciones", []))
            a.file_text = meta.get("texto_extraido", [])

        elif t == "imagen":
            # --- Image_Analyzer | Analisis de metadatos de la imagen ---
            meta = Image_Analyzer(p)

            a.width_px = meta.get("ancho_px")
            a.height_px = meta.get("alto_px")
            a.detected_views = meta.get("vistas_detectadas", [])
            a.comments.extend(meta.get("observaciones", []))
            a.file_text = meta.get("texto_extraido", [])
        else:
            a.comments.append("Tipo no soportado por la versión 0.1 (omitido).")

        analyzed.append(a)

    #__________________________________________________________________________
    #   Generacion de informe

    # --- Reporte | Cantidad de archivos por tipo ---
    by_Type: Dict[str, int] = {"pdf": 0, "imagen": 0, "desconocido": 0}

    for a in analyzed:
        by_Type[a.type_detected] = by_Type.get(a.type_detected, 0) + 1

    summary = {"total_archivos": len(analyzed), "por_tipo": by_Type}

    # --- Reporte | Descripcion general del mueble ---
    description = Furniture_Description(analyzed)
    conclusions = {"comentarios": ["Versión inicial: sin evaluación de viabilidad."]}

    # --- Objeto | Reporte final ---
    report_var = Report(
        project=furniture_name,
        scan_path=str(input_dir),
        summary=summary,
        files=analyzed,
        general_description=description,
        conclusions=conclusions,
        module_version=VERSION_MODULO,
        timestamp=now_iso(),
    )

    # --- Convertir | Reporte a texto ---

    report_text = Report_To_Text(report_var)

    # --- MODELO IA | Instructor de modelacion ---
    agente_IA = Instructor_Modelacion()
    report_refined = agente_IA.Report(report_var, report_text)

    #print(report_refined)

    # --- Escribir | Informes en JSON y TXT ---
    p_json, p_txt = Write_Outputs(report_refined, outputs_root, furniture_name)

    print(f"[hecho] Informe JSON: {p_json}")
    print(f"[hecho] Informe TXT : {p_txt}")

    return p_txt