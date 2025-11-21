from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from annotated_types import doc
import fitz  # PyMuPDF
import sys

# === IMPORTACIONES PROPIAS ===
from utils.keywords import VIEWS_KEYWORDS
from instructor_modelacion.analyzers.ocr_reader import Extract_Text_OCR

"""
    Analiza un PDF:
      - páginas
      - ¿es vectorial?
      - ¿hay texto embebido o visible por OCR?
      - vistas detectadas (texto directo u OCR)
"""
def PDF_Analyzer(path: Path) -> Dict[str, Any]:

    # --- Inicializacion | Diccionario de datos ---
    data: Dict[str, Any] = {
        "paginas": 0,
        "es_vectorial": None,
        "tiene_texto": None,
        "vistas_detectadas": [],
        "observaciones": [],
        "texto_extraido": "",
    }

    # --- PDF To Image ---

    PDF_To_Image(pdf_path=path)

    # --- Apertura | Documento PDF ---
    try:
        doc = fitz.open(str(path))
    except Exception as e:
        data["observaciones"].append(f"No se pudo abrir el PDF: {e}")
        return data

    # --- Analisis | Paginas del PDF ---
    num_pages = doc.page_count 
    data["paginas"] = num_pages

    # --- Variables auxiliares ---
    any_vector = False
    any_text = False
    detected_views: List[str] = []

    # --- 1) Revisión normal (texto digital/vectorial) ---
    for i in range(num_pages):
        try:
            # --- Extraccion | Texto del PDF ---
            page = doc.load_page(i)
            text = page.get_text("text") or ""
            #print(f"Texto: {text}")

            # --- Si: se extrajo texto | Busque informacion de vistas ---
            if text.strip():
                any_text = True
                detected_views.extend(DetectViews_By_Text(text))
                data["texto_extraido"] = " ".join(text)
            
            # --- Extraccion | Dibujos/elementos vectoriales ---
            drawings = page.get_drawings()
            #print(f"Dibujos: {drawings}")

            if drawings and len(drawings) > 0:
                any_vector = True
            
            # --- Extraccion | Imagenes rasterizadas ---
            imgs = page.get_images(full=True)
            #print(f"Imagenes: {imgs}")

            # xref = imgs[0][0]  # ID de la imagen
            # pix = fitz.Pixmap(doc, xref)
            # pix.save("imagen_extraida.png")

            if imgs and not drawings:
                data["observaciones"].append(f"Página {i+1} contiene imágenes rasterizadas.")

        except Exception as e:
            data["observaciones"].append(f"Falla al analizar página {i+1}: {e}")

    # --- 2) Revision por OCR ---
    if not any_text:
        data["observaciones"].append("No se encontró texto embebido; aplicando OCR...")

        text_OCR = Extract_Text_OCR(path)
        #print(f"Texto OCR: {text_OCR}")
        concat_text = " ".join(text_OCR)

        if concat_text.strip():
            any_text = True
            views_ocr = DetectViews_By_Text(concat_text)
            detected_views.extend(views_ocr)

            data["texto_extraido"] = concat_text

            # --- Deteccion | Cotas en el texto OCR ---
            if any(u in concat_text.lower() for u in ["mm", "cm"]):
                data["observaciones"].append("Se detectan cotas en el OCR (mm/cm).")
        else:
            data["observaciones"].append("OCR no detectó texto legible.")

    data["vistas_detectadas"] = sorted(set(detected_views))
    data["es_vectorial"] = any_vector
    data["tiene_texto"] = any_text

    # --- Observaciones generales ---
    if any_vector:
        data["observaciones"].append("Se detectaron elementos vectoriales (paths/drawings).")
    else:
        data["observaciones"].append("No se detectaron elementos vectoriales.")
    if any_text:
        data["observaciones"].append("Se encontró texto (directo u OCR).")

    try:
        doc.close()
    except Exception:
        pass

    #print(data["texto_extraido"])

    return data

"""
    DetectViews_By_Text():
    Funcion auxiliar para detectar vistas en el texto extraido.
    
    - texto | str: Texto extraido.
    - *return* | List[str]: Lista de vistas detectadas
"""
def DetectViews_By_Text(texto: str) -> List[str]:
    views = []

    for v, words in VIEWS_KEYWORDS.items():
        t = texto.lower()

        # --- Compara | Texto con palabras clave ---
        if any(p in t for p in words):
            views.append(v)

    return views

"""
"""
def PDF_To_Image(pdf_path: Path, dpi: int = 150):
    carpeta_salida = pdf_path.parent
    nombre_base = pdf_path.stem
    
    doc = fitz.open(str(pdf_path))
    contador = 0
    
    # Si no hay imágenes, convertir páginas
    if contador == 0:
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            zoom = dpi / 65
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            
            output = carpeta_salida / f"{nombre_base}_image_{page_num+1}.png"
            pix.save(str(output))
            contador += 1
    
    doc.close()
    print(f"✅ {contador} imágenes guardadas en: {carpeta_salida}")