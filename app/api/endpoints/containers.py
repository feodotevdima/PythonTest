from fastapi import APIRouter, Depends, status
from typing import List, Optional
from decimal import Decimal

from app.schemas.container import ContainerResponse, ContainerCreate
from app.api.dependencies import get_current_user, get_container_service
from app.schemas.user import UserResponse

router = APIRouter(prefix="/api/containers", tags=["containers"])

@router.get("", response_model=List[ContainerResponse])
def search_containers(
    q: Optional[str] = None,
    container_service=Depends(get_container_service),
    current_user: UserResponse = Depends(get_current_user)
):

    return container_service.search_containers(q)

@router.get("/by-cost", response_model=List[ContainerResponse])
def search_containers_by_cost(
    cost: Optional[Decimal] = None,
    min_cost: Optional[Decimal] = None,
    max_cost: Optional[Decimal] = None,
    container_service=Depends(get_container_service),
    current_user: UserResponse = Depends(get_current_user)
):

    return container_service.search_by_cost(
        float(cost) if cost else None,
        float(min_cost) if min_cost else None,
        float(max_cost) if max_cost else None
    )

@router.post("", response_model=ContainerResponse, status_code=status.HTTP_201_CREATED)
def create_container(
    container: ContainerCreate,
    container_service=Depends(get_container_service),
    current_user: UserResponse = Depends(get_current_user)
):

    return container_service.create_container(container)