from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional

"""
    File_Analyzed:
    Objeto que representa la informacion primordial de un archivo analizado.
"""
@dataclass
class File_Analyzed:
    name: str
    extension: str
    path: str
    type_detected: str
    is_vector: Optional[bool] = None
    pages: Optional[int] = None
    detected_views: List[str] = field(default_factory=list)
    has_text: Optional[bool] = None
    comments: List[str] = field(default_factory=list)
    width_px: Optional[int] = None
    height_px: Optional[int] = None

"""
    Report:
    Objeto que representa el informe presentado.
"""
@dataclass
class Report:
    project: str
    scan_path: str
    summary: Dict
    files: List[File_Analyzed]
    general_description: str
    conclusions: Dict
    module_version: str
    timestamp: str
