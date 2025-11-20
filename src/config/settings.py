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

# ======== RUTAS PRINCIPALES =========

ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"
SRC_DIR = ROOT_DIR / "src"

# ======== RUTAS MODELOS STARGPT =========

ANALISTA_PIEZAS_PATH = str(SRC_DIR / "analista_piezas")


LOGO_DIR = str(ICONS_DIR / "all_star_logo.svg")

OPEN_AI_LOGO_DIR = str(ICONS_DIR / "openAI.svg")
ANALISTA_PIEZAS_ICON_DIR = str(ICONS_DIR / "analista_piezas.svg")
INSTRUCTOR_ICON_CB = str(ICONS_DIR / "instructor.svg")
ANALISTA_ICON_CB = str(ICONS_DIR / "analista.svg")
SUPERVISOR_ICON_CB = str(ICONS_DIR / "supervisor.svg")

IA_ICON_DIR = str(ICONS_DIR / "AI_icon.svg")

PDF_ICON_DIR = str(ICONS_DIR / "pdf_file.svg")
IMAGE_ICON_DIR = str(ICONS_DIR / "images.svg")
FILE_ICON_DIR = ANALISTA_PIEZAS_ICON_DIR

UPLOAD_ICON_DIR = str(ICONS_DIR / "upload.svg")

ARROW_ICON_CHAT_TOPBAR = str(ICONS_DIR / "Dropdown.svg")

FOLDER_ICON_DIR = str(ICONS_DIR / "folder.svg")

CARD_TOKENS_DIR = str(ICONS_DIR / "diagram_bar.svg")
CARD_COST_DIR = str(ICONS_DIR / "dolar_icon.svg")

ONEDRIVE_CARPENTRY_DIR = str(Path.home() / "OneDrive" / "Carpintería")
ONEDRIVE_MODELS_DIR = str(Path.home() / "OneDrive" / "Carpintería" / "Modelos Produccion")
ONEDRIVE_PROJECTS_DIR = str(Path.home() / "OneDrive" / "Carpintería" / "Proyectos")