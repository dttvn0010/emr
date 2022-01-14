from typing import Optional
from dto import BaseDto

class DepartmentDto(BaseDto):
    id: Optional[int]
    parent_id: Optional[int]
    name: str