from __future__ import annotations
from pathlib import Path
import filetype # Libreria externa para deteccion de tipos de archivo

# === CONSTANTES | Tipos de archivo soportados ===
PDF_EXT = {".pdf"}
IMG_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}

"""
    Scan_InputFolder():
    Funcion encargada de escanear y enlistar los archivos en la carpeta de entrada.

    - input_dir | Path: Ruta de la carpeta de entrada.
    - *return* | list[Path]: Lista de rutas de los archivos encontrados
"""
def Scan_InputFolder(input_dir: Path) -> list[Path]:
    # --- Verificar | Carpeta de entrada existente ---
    if not input_dir.exists():
        raise FileNotFoundError(f"No existe la carpeta de entrada: {input_dir}")
    
    # --- Escanear | Archivos en la carpeta de entrada ---
    files = [p for p in input_dir.rglob("*") if p.is_file()]
    print(f"[scanner] Archivos encontrados: {len(files)}")

    return files

"""
    Guess_Type():
    Funcion encargada de adivinar el tipo de archivo de la ruta entregada.

    - path | Path: Ruta del archivo a analizar.
    - *return* | str: Tipo de archivo detectado (pdf, imagen, desconocido)
"""
def Guess_Type(path: Path) -> str:
    # --- Extraer | Extension del archivo ---
    ext = path.suffix.lower()

    # --- Filtros | Extensiones basicas/conocidas ---
    if ext in PDF_EXT: 
        return "pdf"
    if ext in IMG_EXT: 
        return "imagen"
    
    # --- Deteccion | Tipo de archivo mediante [filetype] ---
    try:
        kind = filetype.guess(str(path))

        if kind:
            if kind.mime == "application/pdf": 
                return "pdf"
            if kind.mime.startswith("image/"):  
                return "imagen"
    except Exception:
        pass

    return "desconocido"