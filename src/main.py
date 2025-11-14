from pathlib import Path
import sys

# === CONFIGURACIÓN MANUAL ===
NOMBRE_MUEBLE = "Mueble TV"

# === PREPARACIÓN DEL ENTORNO ===
BASE = Path(__file__).resolve().parents[1]  # Ruta del proyecto → /DESPIEZADOR IA/
PKG_DIR = BASE / "instructor_modelacion"    # Ruta del paquete-modelo actual → /instructor_modelacion/
sys.path.insert(0, str(PKG_DIR))            # Añadir proyecto actual al path de importaciones

# === IMPORTACIONES PROPIAS ===
from instructor_modelacion.cli import Run_Instructor
from analista_piezas.cli import Run_Analyst

def main():
    # --- Rutas base del proyecto ---
    project_root = BASE                                         # → /DESPIEZADOR IA/
    input_dir = project_root / "data" / "input" / NOMBRE_MUEBLE # → /data/input/mueble_actual/
    output_dir = project_root / "outputs" / NOMBRE_MUEBLE       # → /outputs/mueble_actual/

    # --- INSTRUCTOR DE MODELACION ---
    print("========== INSTRUCTOR DE MODELACIÓN ==========")
    print(f"Proyecto raíz  : {project_root}")
    print(f"Mueble         : {NOMBRE_MUEBLE}")
    print(f"Ruta de entrada: {input_dir}")
    print(f"Ruta de salida : {output_dir}")
    print("==============================================")

    #report_dir = Run_Instructor(input_dir, output_dir)
    report_dir = r"C:\Users\autom\Desktop\CARPINTERIA\STAR GPT\Despiezador IA\outputs\Mueble escritorio\Mueble TV_report.txt"

    # --- ANALISTDA DE PIEZAS ---
    print("========== ANALISTA DE PIEZAS ==========")
    print(f"Proyecto raíz  : {project_root}")
    print(f"Mueble         : {NOMBRE_MUEBLE}")
    print(f"Ruta del reporte: {report_dir}")
    print(f"Ruta de salida : {output_dir}")
    print("==============================================")

    Run_Analyst(input_dir, output_dir, report_dir, NOMBRE_MUEBLE)

if __name__ == "__main__":
    main()