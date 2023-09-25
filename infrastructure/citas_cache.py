import datetime
from typing import Optional, Tuple

from models.citas_query_params import CitasQueryParams

__cache = {}
lifetime_in_minutes = 0.25


def get_appointments(q_params: CitasQueryParams) -> Optional[dict]:
    key = __create_key(q_params)
    data: dict = __cache.get(key)
    if not data:
        return None

    last = data['time']
    dt = datetime.datetime.now() - last
    if dt / datetime.timedelta(seconds=60) < lifetime_in_minutes:
        return data['value']

    del __cache[key]
    return None


def set_appointments(q_params: CitasQueryParams, value: list):
    key = __create_key(q_params)
    data = {
        'time': datetime.datetime.now(),
        'value': value
    }
    __cache[key] = data
    __clean_out_of_date()


def __create_key(q_params: CitasQueryParams) -> Tuple[str, str, str, str]:
    if not q_params.fecha_inicio:
        raise Exception("fecha_inicio is required")

    id_estado = q_params.id_estado
    id_sucursal = q_params.id_sucursal
    fecha_termino = q_params.fecha_termino

    if not id_estado:
        id_estado = ""
    if id_sucursal:
        id_sucursal = ""
    if fecha_termino:
        fecha_termino = ""

    return str(q_params.fecha_inicio).strip().lower(), str(id_estado).strip().lower(), str(id_sucursal).strip().lower(), str(fecha_termino).strip().lower()


def __clean_out_of_date():
    for key, data in list(__cache.items()):
        dt = datetime.datetime.now() - data.get('time')
        if dt / datetime.timedelta(seconds=60) > lifetime_in_minutes:
            del __cache[key]