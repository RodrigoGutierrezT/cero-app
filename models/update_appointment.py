from pydantic import BaseModel
from typing import Optional

class UpdateAppointment(BaseModel):
    id_estado: int