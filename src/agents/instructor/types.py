from pydantic import BaseModel

#_______________________________________________________________
# INSTRUCTOR DE MODELACION

class FileResult(BaseModel):
    name: str
    detected_views: list[str]
    has_text: bool
    comments: list[str]

class Conclusions(BaseModel):
    estado: str
    razones: list[str]

class ReportAIResult(BaseModel):
    files: list[FileResult]
    general_description: str
    conclusions: Conclusions