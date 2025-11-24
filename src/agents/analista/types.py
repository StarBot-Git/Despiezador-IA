from pydantic import BaseModel

#_______________________________________________________________
# ANALISTA DE PIEZAS

class Viability(BaseModel):
    percentage: int
    reason: str

class Detail(BaseModel):
    doors: int
    drawers: int
    shelves: int
    related_to: str

class Components(BaseModel):
    name: str
    type_component: str
    quantity: int
    detail: Detail

class Disassemble(BaseModel):
    message: str
    type_furniture: str
    components: list[Components]
    configuration: str
    comments: str
    viability: Viability

#_______________________________________________________________