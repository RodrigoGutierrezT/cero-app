from models.validation_error import ValidationError 

def validate_positive_int(num):
    if num <= 0:
        error = f"Invalid id {num}, must be a positive number"
        raise ValidationError(status_code=400, error_msg=error)