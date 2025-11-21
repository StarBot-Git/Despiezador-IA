from pathlib import Path

# =======================
# APP INFO
# =======================

APP_NAME = "Star GPT - WoodWork"

# =======================
# RUTAS BASE DEL PROYECTO
# =======================

ROOT_DIR = Path(__file__).resolve().parents[2]

ASSETS_DIR = ROOT_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"
SRC_DIR = ROOT_DIR / "src"