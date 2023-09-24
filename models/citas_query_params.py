from pydantic import BaseModel
from datetime import date
from typing import Optional

class CitasQueryParams(BaseModel):
    fecha_inicio: date
    fecha_termino: Optional[date] = None
    id_estado: Optional[int] = None
    id_sucursal: Optional[int] = None