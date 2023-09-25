from models.citas_query_params import CitasQueryParams
from models.validation_error import ValidationError 

def validate_params(q_params: CitasQueryParams):

    valid_sucursales = [1, 2, 3, 4]

    if q_params.fecha_termino and q_params.fecha_termino < q_params.fecha_inicio:
        error = f"Invalid fecha_termino {q_params.fecha_termino}, must be a date after fecha_inicio {q_params.fecha_inicio}"
        raise ValidationError(status_code=400, error_msg=error)
    
    if q_params.id_sucursal and q_params.id_sucursal not in valid_sucursales:
        error = f"Invalid id_sucursal {q_params.id_sucursal}, must be one of the following ids {valid_sucursales}"
        raise ValidationError(status_code=400, error_msg=error)