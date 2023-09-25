from models.validation_error import ValidationError


def validate_cancel_appointment(id_estado: int, appointment: dict):

    valid_cancel_appointment_ids = [1, 9, 14, 26]

    if id_estado not in valid_cancel_appointment_ids:
            error = f"id_estado {id_estado} Must be on of the following values {valid_cancel_appointment_ids}"
            raise ValidationError(error, status_code=400)

    if appointment.get('estado_anulacion') == 1:
        error = f"Appointment {appointment.get('id')} is already Cancelled"
        raise ValidationError(error, status_code=409)

def validate_confirm_appointment(id_estado: int, appointment: dict):

    valid_confirm_appointment_ids = [3, 16, 25]

    if id_estado not in valid_confirm_appointment_ids:
            error = f"id_estado {id_estado} Must be on of the following values {valid_confirm_appointment_ids}"
            raise ValidationError(error, status_code=400)

    if appointment.get('estado_anulacion') == 1:
        error = f"Appointment {appointment.get('id')} is already Cancelled"
        raise ValidationError(error, status_code=409)