from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user: UserCreate) -> User:
        db_user = User(
            username=user.username,
            password_hash=get_password_hash(user.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()