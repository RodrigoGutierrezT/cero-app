from typing import Optional, List
import httpx
from models.citas_query_params import CitasQueryParams
from models.validation_error import ValidationError
from utilities.build_query_string import build_query_string
from datetime import datetime

api_key: Optional[str] = None
base_url: str = "https://api.dentalink.healthatom.com/api/v1/citas"

async def get_appointments(q_params: CitasQueryParams) -> List[dict]:

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
            print(request.url)

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
            return filtered_data

        return data
