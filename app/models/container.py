from sqlalchemy import Column, Integer, String, Numeric, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base


class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    container_number = Column(String(11), unique=True, index=True, nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index('idx_container_number', container_number),
        Index('idx_cost', cost),
    )
