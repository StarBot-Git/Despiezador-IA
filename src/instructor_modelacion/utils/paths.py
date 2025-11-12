from __future__ import annotations
from pathlib import Path

"""
    Normalize_Path():
    Normaliza la ruta recibida; expande el ~ y resuelve rutas relativas.

    - p: Ruta a normalizar.
"""
def Normalize_Path(p):
    return Path(p).expanduser().resolve()

"""
    Ensure_OutputsRoot():
    Asegura que la ruta de salida exista; si no, la crea.

    - out_root: Teorica ruta de salida.
"""
def Ensure_OutputsRoot(out_root):
    out_root = Path(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    
    return out_root