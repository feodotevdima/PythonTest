from pydantic import BaseModel, validator, constr
from typing import Optional
from decimal import Decimal
import re
from datetime import datetime


class ContainerBase(BaseModel):
    container_number: constr(max_length=11)
    cost: Decimal

    @validator('container_number')
    def validate_container_number(cls, v):
        pattern = r'^[A-Z]{3}U\d{7}$'
        if not re.match(pattern, v):
            raise ValueError('Container number must be in format: 3 uppercase letters + U + 7 digits')
        return v

    @validator('cost')
    def validate_cost(cls, v):
        if v <= 0:
            raise ValueError('Cost must be positive')
        return round(v, 2)


class ContainerCreate(ContainerBase):
    pass


class ContainerResponse(ContainerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ContainerSearch(BaseModel):
    q: Optional[str] = None


class CostFilter(BaseModel):
    cost: Optional[Decimal] = None
    min_cost: Optional[Decimal] = None
    max_cost: Optional[Decimal] = None

    @validator('min_cost', 'max_cost', 'cost')
    def validate_cost_values(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Cost values must be positive')
        return v