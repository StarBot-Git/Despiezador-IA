from __future__ import annotations
from typing import List
from .utils.types import File_Analyzed
from instructor_modelacion.utils.keywords import Keyword_Match, FURNITURE_KEYWORDS

def Furniture_Description(files: List[File_Analyzed]) -> str:
    corpus = []
    views = set()

    for a in files:
        corpus.append(a.name)
        corpus.extend(a.detected_views)
        views.update(a.detected_views)
        
    text = " ".join(corpus).lower()
    types = Keyword_Match(text, FURNITURE_KEYWORDS)

    parts = []

    if types:
        parts.append(f"Se identifica relación con: {', '.join(sorted(types))}.")
    if views:
        parts.append(f"Se detectan vistas: {', '.join(sorted(views))}.")
    if not parts:
        parts.append("No se identifican palabras clave; revisar manualmente.")
        
    return " ".join(parts)