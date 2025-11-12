from pathlib import Path
import sys
# Agrega la ruta padre (/src) al sys.path
BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from instructor_modelacion.analyzers.ocr_reader import extraer_texto_pdf_ocr

# Ruta al PDF (ajústala si estás en otra carpeta)
pdf_path = Path(r"C:\Users\autom\Desktop\CARPINTERIA\STAR GPT\Despiezador IA\data\input\Mueble escobero\Plano 1.pdf")

print(f"Probando OCR en: {pdf_path}")
textos = extraer_texto_pdf_ocr(pdf_path)

print("\n========= RESULTADO OCR =========")
for i, t in enumerate(textos, 1):
    print(f"\n--- Página {i} ---")
    print(t[:1500])  # mostramos los primeros 1500 caracteres para no saturar
print("=================================")