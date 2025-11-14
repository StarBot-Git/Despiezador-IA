from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from utils.types import Report, File_Analyzed

"""
"""
def report_to_dict(report: Report) -> Dict:
    return {
        "proyecto": report.project,
        "ruta_escaneo": report.scan_path,
        "resumen": report.summary,
        "archivos": [a.__dict__ for a in report.files],
        "descripcion_general_mueble": report.general_description,
        "conclusiones": report.conclusions,
        "version_modulo": report.module_version,
        "timestamp": report.timestamp,
    }

"""
"""
def Report_To_Text(report: Report) -> str:
    lines = []
    lines.append(f"Proyecto: {report.project}")
    lines.append(f"Ruta de escaneo: {report.scan_path}")
    lines.append(f"Versión módulo: {report.module_version}")
    lines.append(f"Fecha: {report.timestamp}")
    lines.append("\n[Resumen]")
    lines.append(json.dumps(report.summary, ensure_ascii=False, indent=2))
    lines.append("\n[Archivos]")

    for f in report.files:
        lines.append(f"- {f.name} ({f.type_detected})")
        if f.type_detected == "pdf":
            lines.append(f"  páginas={f.pages}, vectorial={f.is_vector}, texto={f.has_text}")
        if f.type_detected == "imagen":
            lines.append(f"  tamaño={f.width_px}x{f.height_px}px")
        if f.detected_views:
            lines.append(f"  vistas={', '.join(f.detected_views)}")
        if f.comments:
            lines.append(f"  obs={'; '.join(f.comments)}")
        if f.file_text:
            lines.append("\n[Texto extraído del archivo]")
            lines.append(f.file_text)

    lines.append("\n[Conclusiones]")
    lines.append(json.dumps(report.conclusions, ensure_ascii=False, indent=2))

    return "\n".join(lines)

"""
"""
def Write_Outputs(report: Report, out_root: Path, furniture_name: str) -> tuple[Path, Path]:
    out_root.mkdir(parents=True, exist_ok=True)

    # --- Inicializacion | Nombre del mueble y rutas ---
    base = f"{furniture_name}_report"
    p_json = out_root / f"{base}.json"
    p_txt  = out_root / f"{base}.txt"
    

    # --- Escritura | Archivos JSON y TXT ---
    with open(p_json, "w", encoding="utf-8") as f:
        json.dump(report_to_dict(report), f, ensure_ascii=False, indent=2)

    # p_aux_txt = out_root / f"{base}_PDF_TEXT.txt"
    # with open(p_aux_txt, "w", encoding="utf-8") as f:
    #     f.write(report.files[0].file_text)

    with open(p_txt, "w", encoding="utf-8") as f:
        f.write(f"Proyecto: {report.project}\n")
        f.write(f"Ruta de escaneo: {report.scan_path}\n")
        f.write(f"Versión módulo: {report.module_version}\n")
        f.write(f"Fecha: {report.timestamp}\n\n")
        f.write("[Resumen]\n")
        f.write(json.dumps(report.summary, ensure_ascii=False, indent=2))
        f.write("\n\n[Descripción general del mueble]\n")
        f.write(report.general_description + "\n\n")
        f.write("[Archivos]\n")

        for a in report.files:
            f.write(f"- {a.name} ({a.type_detected})\n")
            if a.type_detected == "pdf":
                f.write(f"  páginas={a.pages}, vectorial={a.is_vector}, texto={a.has_text}\n")
            if a.type_detected == "imagen":
                f.write(f"  tamaño={a.width_px}x{a.height_px}px\n")
            if a.detected_views:
                f.write(f"  vistas={', '.join(a.detected_views)}\n")
            if a.comments:
                f.write(f"  obs={'; '.join(a.comments)}\n")
        
        f.write("\n[Conclusiones]\n")
        f.write(json.dumps(report.conclusions, ensure_ascii=False, indent=2))
        f.write("\n")
    return p_json, p_txt

"""
    now_iso():
    Retorna la fecha y hora actual en formato ISO 8601.
"""
def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")