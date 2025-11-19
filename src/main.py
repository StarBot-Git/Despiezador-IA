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
from supervisor_piezas.cli import Run_Supervisor

def main():
    # --- Rutas base del proyecto ---
    project_root = BASE                                        # → /DESPIEZADOR IA/
    input_dir = project_root / "input" / NOMBRE_MUEBLE         # → /input/mueble_actual/
    output_dir = project_root / "output" / NOMBRE_MUEBLE       # → /output/mueble_actual/

    # --- INSTRUCTOR DE MODELACION ---
    print("┌──────────────────────────────────────────┐")
    print("         INSTRUCTOR DE MODELACIÓN\n")
    print(f"▣ Proyecto raíz  : {project_root}")
    print(f"▣ Mueble         : {NOMBRE_MUEBLE}")
    print(f"▣ Ruta de entrada: {input_dir}")
    print(f"▣ Ruta de salida : {output_dir}")
    print("\n└───────────────────────────────────────────┘")

    #report_dir = Run_Instructor(input_dir, output_dir)
    report_dir = r"C:\Users\autom\Desktop\CARPINTERIA\STAR GPT\Despiezador IA\output\Mueble TV\Mueble TV_report.txt"

    # --- ANALISTDA DE PIEZAS ---
    print("┌──────────────────────────────────────────┐")
    print("         ANALISTA DE PIEZAS\n")
    print(f"▣ Proyecto raíz  : {project_root}")
    print(f"▣ Mueble         : {NOMBRE_MUEBLE}")
    print(f"▣ Ruta del reporte: {report_dir}")
    print(f"▣ Ruta de salida : {output_dir}")
    print("\n└───────────────────────────────────────────┘")

    file_JSON, file_data = Run_Analyst(input_dir, output_dir, report_dir, NOMBRE_MUEBLE)
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