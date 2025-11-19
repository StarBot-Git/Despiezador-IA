from dataclasses import dataclass
from pathlib import Path

# ======== IDENTIDAD VENTANA =========

APP_NAME = "Star GPT - WoodWork"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

# ======== TEMA ==========

THEME = "light"  # Opciones: "light", "dark"

BLUE_ALL_STAR = "#133855"
ORANGE_ALL_STAR = "#C7664C"
WHITE_ALL_STAR = "#FFFFFF"
THEME_LIGHT = "#000000"

# --- LIGHT | DARK ---

BACKGROUND_LIGHT = "#FFFFFF"
FONT_LIGHT = "#000000"

BACKGROUND_DARK = "#000000"
FONT_DARK = "#FFFFFF"

# ======== RUTAS =========

ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"

LOGO_DIR = str(ICONS_DIR / "all_star_logo.svg")
ANALISTA_PIEZAS_ICON_DIR = str(ICONS_DIR / "analista_piezas.svg")
INSTRUCTOR_ICON_CB = str(ICONS_DIR / "instructor.svg")
ANALISTA_ICON_CB = str(ICONS_DIR / "analista.svg")
SUPERVISOR_ICON_CB = str(ICONS_DIR / "supervisor.svg")

PDF_ICON_DIR = ANALISTA_PIEZAS_ICON_DIR
IMAGE_ICON_DIR = ANALISTA_PIEZAS_ICON_DIR
FILE_ICON_DIR = ANALISTA_PIEZAS_ICON_DIR

ONEDRIVE_CARPENTRY_DIR = str(Path.home() / "OneDrive" / "Carpintería")
ONEDRIVE_MODELS_DIR = str(Path.home() / "OneDrive" / "Carpintería" / "Modelos Produccion")
ONEDRIVE_PROJECTS_DIR = str(Path.home() / "OneDrive" / "Carpintería" / "Proyectos")