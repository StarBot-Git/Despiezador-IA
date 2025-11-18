import fitz
from pathlib import Path

def extraer_imagenes_pdf(ruta_pdf: str, dpi: int = 150):
    pdf_path = Path(ruta_pdf)
    carpeta_salida = pdf_path.parent
    nombre_base = pdf_path.stem
    
    doc = fitz.open(str(pdf_path))
    contador = 0
    
    # Intentar extraer imágenes embebidas
    # for page_num in range(doc.page_count):
    #     page = doc.load_page(page_num)
    #     images = page.get_images(full=True)
        
    #     for img_index, img in enumerate(images):
    #         try:
    #             xref = img[0]
    #             pix = fitz.Pixmap(doc, xref)
                
    #             if pix.n - pix.alpha > 3:  # CMYK
    #                 pix = fitz.Pixmap(fitz.csRGB, pix)
                
    #             output = carpeta_salida / f"{nombre_base}_img{contador+1}.png"
    #             pix.save(str(output))
    #             contador += 1
    #         except:
    #             pass
    
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

# Uso directo
extraer_imagenes_pdf(r"C:\Users\autom\Desktop\CARPINTERIA\STAR GPT\Despiezador IA\input\Mueble TV\Plano 1.pdf")