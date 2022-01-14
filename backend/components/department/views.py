from typing import List
from fastapi import APIRouter, Depends, Response, status
from pydantic import ValidationError

from db import Department
from auth.auth import get_current_user
from constants import Permissions
from utils import dump_error, check_permission, copy_dict_to_object

from .dto import DepartmentDto

router = APIRouter(prefix='/department', tags=["department"])

@router.post("/")
async def create_department(data:dict, response: Response, current_user=Depends(get_current_user)):
    if not check_permission(current_user, Permissions.ADD_DEPARTMENT.name, response):
        return {'error': 'User has no permission'}
    
    try:
        dto = DepartmentDto(**data)
    except ValidationError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return dump_error(e)
    
    department = Department(**dto.dict())
    department.save()
    return DepartmentDto.from_orm(department)

@router.put('/{id}')
async def update_department(id:int, data:dict, response: Response, current_user=Depends(get_current_user)):
    if not check_permission(current_user, Permissions.CHANGE_DEPARTMENT.name, response):
        return {'error': 'User has no permission'}

    try:
        dto = DepartmentDto(**data, id=id)
    except ValidationError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return dump_error(e)

    department = Department.get(id)
    copy_dict_to_object(dto.dict(), department)
    department.save()
    return DepartmentDto.from_orm(department)

@router.delete('/{id}')
async def delete_department(id: int, response: Response, current_user=Depends(get_current_user)):
    if not check_permission(current_user, Permissions.DELETE_DEPARTMENT.name, response):
        return {'error': 'User has no permission'}

    department = Department.get(id)
    department.delete_instance()
    return {'success': True}

@router.get('/search', response_model=List[DepartmentDto])
async def search_department(keyword: str=''):
    return list(
        Department.select().where(
            Department.name.contains(keyword)
        )
    )