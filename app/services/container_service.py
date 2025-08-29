from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.container_repository import ContainerRepository
from app.schemas.container import ContainerCreate
from app.core.exceptions import ContainerAlreadyExistsException


class ContainerService:
    def __init__(self, db: Session):
        self.container_repository = ContainerRepository(db)

    def create_container(self, container: ContainerCreate):
        existing_container = self.container_repository.get_by_number(container.container_number)
        if existing_container:
            raise ContainerAlreadyExistsException()

        return self.container_repository.create(container)

    def search_containers(self, q: str = None, limit: int = 50):
        return self.container_repository.search_by_number(q, limit)

    def search_by_cost(self, cost: float = None, min_cost: float = None, max_cost: float = None):
        if cost is None and min_cost is None and max_cost is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one cost parameter is required"
            )

        return self.container_repository.search_by_cost(cost, min_cost, max_cost)

    def get_all_containers(self, skip: int = 0, limit: int = 100):
        return self.container_repository.get_all(skip, limit)