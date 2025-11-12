from __future__ import annotations
from pathlib import Path
import pytesseract      # Tesseract OCR
import fitz             # PyMuPDF
import cv2              # OpenCV
import numpy as np
from PIL import Image
from typing import List

# === CONFIGURACION TESSERACT ===
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

"""
    Extract_Text_OCR():
    Lee todas las páginas del PDF, convierte cada una a imagen,
    y aplica OCR para extraer texto (útil para PDFs escaneados).
    Retorna una lista con el texto detectado por página.
"""
def Extract_Text_OCR(path_pdf: Path) -> List[str]:
    text_pages = []

    try:
        doc = fitz.open(str(path_pdf))
    except Exception as e:
        print(f"[ocr_reader] No se pudo abrir el PDF: {e}")

        return []

    for i in range(doc.page_count):

        try:
            page = doc.load_page(i)

            # --- Convertir | Pagina PDF a imagen ---
            pix = page.get_pixmap(dpi=300)

            # --- Conversion | Pixmap a imagen PIL y OCR ---
            img_data = np.frombuffer(pix.tobytes(), dtype=np.uint8) # Convierte la imagen en array de bytes
            img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)          # Decodifica el array a imagen OpenCV

            if img is None:
                # --- Fallback case: usa PIL directamente ---
                print(f"[ocr_reader] Fallback: usando PIL para página {i+1}")

                # --- Conversion | pix a imagen PIL ---
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples) 

                # --- OCR | Extraer texto de la imagen con Tesseract ---
                text = pytesseract.image_to_string(image, lang="spa")
            else:
                # --- Preprocesamiento | Escala de grises ---
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # --- Preprocesamiento | Umbralizacion [Pixel > 180 = blanco | Pixel <= 180 = negro] ---
                _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

                # --- OCR | Extraer texto de la imagen con Tesseract ---
                text = pytesseract.image_to_string(thresh, lang="spa")

            text = text.strip()

            text_pages.append(text)
        except Exception as e:
            text_pages.append(f"[Error OCR página {i+1}]: {e}")

    try:
        doc.close()
    except Exception:
        pass
    return text_pages

"""
    Busca si alguna de las palabras clave aparece en los textos OCR.
    Devuelve las que fueron encontradas.
"""
def SearchKeyWords_OCR(texts: List[str], words: List[str]) -> List[str]:
    detected_views = []

    for w in words:
        for t in texts:
            if w.lower() in t.lower():
                detected_views.append(w)
                break
            
    return sorted(set(detected_views))