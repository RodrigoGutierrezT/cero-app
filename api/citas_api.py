import fastapi

from services import dentalink_service

from models.citas_query_params import CitasQueryParams
from models.validation_error import ValidationError
from models.update_appointment import UpdateAppointment

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


@router.put("/api/citas/{id_cita}/cancel", status_code=201)
async def cancelar_cita(id_cita: int , new_data: UpdateAppointment):
    try:
        appointment = await dentalink_service.get_appointment(id_cita)
        new_appointment = await dentalink_service.cancel_appointment(new_data.id_estado, appointment)
        return new_appointment
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as x:
        return fastapi.Response(content=str(x), status_code=500)


@router.put("/api/citas/{id_cita}/confirm", status_code=201)
async def confirmar_cita(id_cita: int , new_data: UpdateAppointment):
    try:
        appointment = await dentalink_service.get_appointment(id_cita)
        new_appointment = await dentalink_service.confirm_appointment(new_data.id_estado, appointment)
        return new_appointment
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as x:
        return fastapi.Response(content=str(x), status_code=500)