from pydantic import BaseModel

#_______________________________________________________________
# PARAMETRIZADOR DE MODULOS

class Dimensions(BaseModel):
    height: float
    width: float
    depth: float
    unit: str

class Viability(BaseModel):
    percentage: int
    reason: str
    missing_data: list[str]

class Pieces(BaseModel):
    name: str
    role: str
    height: float
    width: float
    depth: float
    material: str
    quantity: int

class SubModules(BaseModel):
    name: str
    type: str
    specifications: str
    relative_position: str
    dimensions: Dimensions

class Structure(BaseModel):
    doors: int
    drawers: int
    shelves: int
    cavities: int

class Modules_Description(BaseModel):
    name: str
    type: str
    global_position: str
    dimensions: Dimensions
    structure: Structure
    sub_modules: list[SubModules]
    pieces: list[Pieces]
    assumptions: list[str]
    viability: Viability

class ModuleParametrizationResult(BaseModel):
    parametrizacion: list
    tokens: dict

# class Moduls(BaseModel):
#     modul_desc: list[Modul_Description]

#_______________________________________________________________