import sys

from pathlib import Path
from PySide6.QtWidgets import QApplication

# ====== PREPARACIÓN DEL ENTORNO ======
BASE = Path(__file__).resolve().parents[1]  # Ruta del proyecto → /DESPIEZADOR IA/
sys.path.insert(0, str(BASE))               # Añadir proyecto actual al path de importaciones

# ====== IMPORTACIONES PROPIAS ======
from ui.config import theme
from ui.windows.main_window import MainWindow
import ui.resources.resources_rc


"""
    apply_stylesheet():
    Funcion encargada de aplicar estilo qss a la aplicacion
"""
def apply_stylesheet(app: QApplication) -> None:
    # === Cargar hoja de estilos | style.qss ===
    style_path = Path(__file__).parent / "ui" / "styles" / "style.qss"

    if style_path.exists():
        # === Leer archivo ===
        qss = style_path.read_text(encoding="utf-8")
        
        # === Reemplazar constantes ===
        qss = qss.replace('{{PRIMARY}}', theme.BLUE_ALL_STAR)
        qss = qss.replace('{{SECONDARY}}', theme.WHITE_ALL_STAR)
        qss = qss.replace('{{COMPLEMENTARY}}', theme.ORANGE_ALL_STAR)
        qss = qss.replace('{{FONT_DARK}}', theme.FONT_DARK)
        qss = qss.replace('{{FONT_LIGHT}}', theme.FONT_LIGHT)
        qss = qss.replace('{{BG_DARK}}', theme.BACKGROUND_DARK)
        qss = qss.replace('{{BG_LIGHT}}', theme.BACKGROUND_LIGHT)
        
        # === Aplicar hoja de estilos ===
        app.setStyleSheet(qss)

def main():
    app = QApplication(sys.argv)

    apply_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

    # # --- Rutas base del proyecto ---
    # project_root = BASE                                        # → /DESPIEZADOR IA/
    # input_dir = project_root / "input" / NOMBRE_MUEBLE         # → /input/mueble_actual/
    # output_dir = project_root / "output" / NOMBRE_MUEBLE       # → /output/mueble_actual/

    # # --- INSTRUCTOR DE MODELACION ---
    # print("┌──────────────────────────────────────────┐")
    # print("         INSTRUCTOR DE MODELACIÓN\n")
    # print(f"▣ Proyecto raíz  : {project_root}")
    # print(f"▣ Mueble         : {NOMBRE_MUEBLE}")
    # print(f"▣ Ruta de entrada: {input_dir}")
    # print(f"▣ Ruta de salida : {output_dir}")
    # print("\n└───────────────────────────────────────────┘")

    # #report_dir = Run_Instructor(input_dir, output_dir)
    # report_dir = r"C:\Users\autom\Desktop\CARPINTERIA\STAR GPT\Despiezador IA\output\Mueble TV\Mueble TV_report.txt"

    # # --- ANALISTDA DE PIEZAS ---
    # print("┌──────────────────────────────────────────┐")
    # print("         ANALISTA DE PIEZAS\n")
    # print(f"▣ Proyecto raíz  : {project_root}")
    # print(f"▣ Mueble         : {NOMBRE_MUEBLE}")
    # print(f"▣ Ruta del reporte: {report_dir}")
    # print(f"▣ Ruta de salida : {output_dir}")
    # print("\n└───────────────────────────────────────────┘")

    # file_JSON, file_data = Run_Analyst(input_dir, output_dir, report_dir, NOMBRE_MUEBLE)
    # file_JSON = r"C:\Users\autom\Desktop\CARPINTERIA\STAR GPT\Despiezador IA\output\Mueble TV\Mueble TV_piezas.json"
    # file_data = {}

    # # --- SUPERVISOR DE PIEZAS ---
    # print("┌──────────────────────────────────────────┐")
    # print("         SUPERVISOR DE PIEZAS\n")
    # print(f"▣ Proyecto raíz  : {project_root}")
    # print(f"▣ Mueble         : {NOMBRE_MUEBLE}")
    # print(f"▣ Ruta de salida : {output_dir}")
    # print("\n└───────────────────────────────────────────┘")

    # Run_Supervisor(input_dir=input_dir, output_root=output_dir, file_pieces_JSON=file_JSON, furniture_name=NOMBRE_MUEBLE, files=file_data)

if __name__ == "__main__":
    main()