from typing import Optional, List
import httpx
from models.citas_query_params import CitasQueryParams
from models.validation_error import ValidationError
from infrastructure import citas_cache
from utilities.build_query_string import build_query_string
from utilities.validate_query_params import validate_params
from utilities.validate_positive_int import validate_positive_int
from utilities.validate_appointments import validate_cancel_appointment
from datetime import datetime

api_key: Optional[str] = None
base_url: str = "https://api.dentalink.healthatom.com/api/v1/citas"

async def get_appointments(q_params: CitasQueryParams) -> List[dict]:

    validate_params(q_params)

    if cache_data := citas_cache.get_appointments(q_params):
        return cache_data

    params = {
        "fecha": {"gte": q_params.fecha_inicio.strftime("%Y-%m-%d")}
    }

    if q_params.id_estado:
        params["id_estado"] = {"eq": q_params.id_estado}
    if q_params.id_sucursal:
        params["id_sucursal"] = {"eq": q_params.id_sucursal}

    url = base_url+build_query_string(params)
    print(url)
    
    async with httpx.AsyncClient() as client:
        data = []
        headers: dict = {"Authorization": "Token " + api_key}

        while True:
            resp: httpx.Response = await client.get(url, headers=headers)
            request = resp.request

            if resp.status_code == 200:
                res_json = resp.json()
                data.extend(res_json.get("data", []))
                links = res_json.get("links")
                if links:
                    next_link = links.get("next")

                    if next_link:
                        url = next_link
                    else:
                        break
                else:
                    break
            else:
                raise ValidationError(resp.text, status_code=resp.status_code)
        
        if q_params.fecha_termino and data:
            filtered_data = [item for item in data if datetime.strptime(item["fecha"], "%Y-%m-%d").date() <= q_params.fecha_termino]
            citas_cache.set_appointments(q_params, filtered_data)
            return filtered_data

        citas_cache.set_appointments(q_params, data)
        return data


async def get_appointment(id_cita: int) -> dict:

    validate_positive_int(id_cita)

    url = base_url + f"/{id_cita}"

    async with httpx.AsyncClient() as client:
        headers: dict = {"Authorization": "Token " + api_key}
        resp = await client.get(url, headers=headers)
        
        if resp.status_code == 200:
            res_json = resp.json()
            return res_json.get("data", None)
        else:
            raise ValidationError(resp.text, status_code=resp.status_code)

async def cancel_appointment(id_estado: int, appointment: dict):
    
    validate_cancel_appointment(id_estado,appointment)

    url = base_url + f"/{appointment.get('id')}"
    print(url)

    async with httpx.AsyncClient() as client:
        headers: dict = {"Authorization": "Token " + api_key}
        resp = await client.put(url, headers=headers, json={"id_estado": id_estado})
        
        if resp.status_code == 200 or resp.status_code == 201:
            res_json = resp.json()
            return res_json.get("data", None)
        else:
            raise ValidationError(resp.text, status_code=resp.status_code)
