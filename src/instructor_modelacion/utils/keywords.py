VIEWS_KEYWORDS = {
    "frontal": ["frontal", "frente", "vista frontal", "elevación", "alzado"],
    "lateral": ["lateral", "vista lateral", "costado", "perfil"],
    "planta":  ["planta", "superior", "vista superior", "arriba"],
    "isometrica": ["isométrica", "isometrica", "axo", "axonométrica", "3d", "3D"],
    "corte": ["corte", "sección", "seccion", "perfil cortado"],
}

FURNITURE_KEYWORDS = {
    "cocina": ["cocina", "mueble alto", "alacena", "gabinete", "superior"],
    "baño": ["baño", "vanitorio", "lavamanos"],
    "closet": ["clóset", "closet", "armario", "ropero"],
    "tv": ["tv", "entretenimiento", "panel"],
    "oficina": ["oficina", "archivador", "escritorio"],
}

def Keyword_Match(text: str, map: dict[str, list[str]]) -> list[str]:
    t = text.lower()
    match = set()
    for etiqueta, palabras in map.items():
        if any(p.lower() in t for p in palabras):
            match.add(etiqueta)
            
    return list(match)