from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.container import Container
from app.schemas.container import ContainerCreate


class ContainerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_number(self, container_number: str) -> Container:
        return self.db.query(Container).filter(
            Container.container_number == container_number
        ).first()

    def get_by_id(self, container_id: int) -> Container:
        return self.db.query(Container).filter(Container.id == container_id).first()

    def create(self, container: ContainerCreate) -> Container:
        db_container = Container(
            container_number=container.container_number,
            cost=float(container.cost)
        )
        self.db.add(db_container)
        self.db.commit()
        self.db.refresh(db_container)
        return db_container

    def search_by_number(self, q: str = None, limit: int = 50):
        query = self.db.query(Container)
        if q:
            query = query.filter(Container.container_number.contains(q))
        return query.order_by(Container.id).limit(limit).all()

    def search_by_cost(self, cost: float = None, min_cost: float = None, max_cost: float = None):
        query = self.db.query(Container)

        if cost is not None:
            query = query.filter(Container.cost == cost)
        elif min_cost is not None and max_cost is not None:
            query = query.filter(
                and_(
                    Container.cost >= min_cost,
                    Container.cost <= max_cost
                )
            )
        elif min_cost is not None:
            query = query.filter(Container.cost >= min_cost)
        elif max_cost is not None:
            query = query.filter(Container.cost <= max_cost)

        return query.order_by(Container.cost).all()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Container).offset(skip).limit(limit).all()