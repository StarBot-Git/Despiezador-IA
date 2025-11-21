from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from PIL import Image

# === IMPORTACIONES PROPIAS ===
from utils.keywords import VIEWS_KEYWORDS

"""
    Image_Analyzer():
"""
def Image_Analyzer(path: Path) -> Dict[str, Any]:

    # --- Inicializacion | Diccionario de datos ---
    data: Dict[str, Any] = {
        "ancho_px": None,
        "alto_px": None,
        "vistas_detectadas": [],
        "observaciones": [],
    }

    # --- Apertura | Imagen ---
    try:
        with Image.open(path) as im:
            data["ancho_px"], data["alto_px"] = im.size
    except Exception as e:
        data["observaciones"].append(f"No se pudo abrir la imagen: {e}")

        return data

    # --- Deteccion | Vistas desde el nombre del archivo ---
    data["vistas_detectadas"] = Views_From_Filename(path.stem)

    # --- Observaciones | Resolucion de imagen ---
    w, h = data["ancho_px"], data["alto_px"]

    if w and h:
        if min(w, h) < 800:
            data["observaciones"].append("Resolución baja (<800px en el lado menor).")
        elif min(w, h) >= 2000:
            data["observaciones"].append("Resolución alta (>=2000px en el lado menor).")
    return data

"""
    Views_From_Filename():
"""
def Views_From_Filename(name: str) -> List[str]:
    n = name.lower().replace("-", " ").replace("_", " ")
    views = []

    for v, words in VIEWS_KEYWORDS.items():
        if any(p in n for p in words):
            views.append(v)

    return sorted(set(views))