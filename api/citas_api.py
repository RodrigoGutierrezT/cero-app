from typing import Optional
import fastapi

from services import dentalink_service

from models.citas_query_params import CitasQueryParams
from models.validation_error import ValidationError

router = fastapi.APIRouter()

@router.get("/api/citas")
async def citas(q_params: CitasQueryParams = fastapi.Depends()):
    try:
        appointments = await dentalink_service.get_appointments(q_params)
        return appointments
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as x:
        return fastapi.Response(content=str(x), status_code=500)