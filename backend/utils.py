from typing import List
from pydantic import ValidationError
from fastapi import status
from auth.auth import has_privilege

def dump_error(e: ValidationError):
    errors = {}

    for error in e.raw_errors:
        loc = error._loc
        message = str(error.exc)
        if loc not in errors:
            errors[loc] = []
        errors[loc].append(message)

    return errors

def copy_dict_to_object(data: dict, obj: object, exclude_fields: List[str]=[]):
    for k,v in data.items():
        if hasattr(obj, k) and k not in exclude_fields:
            setattr(obj, k, v)

def check_permission(user, permission, response):
    if not has_privilege(user, permission):
        response.status_code = status.HTTP_403_FORBIDDEN
        return False
    
    return True

def validate_not_blank(value: str):
    if not value or value.strip() == '':
        raise ValueError('Trường này là bắt buộc')