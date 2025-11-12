from pathlib import Path
import sys

# === CONFIGURACIÓN MANUAL ===
NOMBRE_MUEBLE = "Mueble escobero"

# === PREPARACIÓN DEL ENTORNO ===
BASE = Path(__file__).resolve().parents[1]  # Ruta del proyecto → /DESPIEZADOR IA/
PKG_DIR = BASE / "instructor_modelacion"    # Ruta del paquete-modelo actual → /instructor_modelacion/
sys.path.insert(0, str(PKG_DIR))            # Añadir proyecto actual al path de importaciones

# === IMPORTACIONES PROPIAS ===
from instructor_modelacion.cli import Run_Instructor

def main():
    # --- Rutas base del proyecto ---
    project_root = BASE                                         # → /DESPIEZADOR IA/
    input_dir = project_root / "data" / "input" / NOMBRE_MUEBLE # → /data/input/mueble_actual/
    output_dir = project_root / "outputs" / NOMBRE_MUEBLE       # → /outputs/mueble_actual/

    # --- Ejecucion del instructor de modelacion ---
    print("========== INSTRUCTOR DE MODELACIÓN ==========")
    print(f"Proyecto raíz  : {project_root}")
    print(f"Mueble         : {NOMBRE_MUEBLE}")
    print(f"Ruta de entrada: {input_dir}")
    print(f"Ruta de salida : {output_dir}")
    print("==============================================")

    Run_Instructor(input_dir, output_dir)

if __name__ == "__main__":
    main()