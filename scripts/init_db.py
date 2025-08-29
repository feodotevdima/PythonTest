import sys
from pathlib import Path
import random
import string

current_dir = Path(__file__).parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))

from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.container import Container
from app.core.security import get_password_hash


def generate_container_number():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=7))
    return f"{letters}U{numbers}"


def init_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:

        users = [
            {"username": "user1", "password": "password1"},
            {"username": "user2", "password": "password2"},
            {"username": "user3", "password": "password3"},
        ]

        created_users = []
        for user_data in users:
            existing_user = db.query(User).filter(
                User.username == user_data["username"]
            ).first()

            if not existing_user:
                user = User(
                    username=user_data["username"],
                    password_hash=get_password_hash(user_data["password"])
                )
                db.add(user)
                created_users.append(user_data["username"])

        container_numbers = set()
        while len(container_numbers) < 10:
            container_numbers.add(generate_container_number())

        created_containers = []
        for number in container_numbers:
            existing_container = db.query(Container).filter(
                Container.container_number == number
            ).first()

            if not existing_container:
                cost = round(random.uniform(100.00, 10000.00), 2)
                container = Container(
                    container_number=number,
                    cost=cost
                )
                db.add(container)
                created_containers.append((number, cost))

        db.commit()

        print("Database initialized successfully!")
        print("\nCreated users:")
        for username in created_users:
            user_data = next(u for u in users if u["username"] == username)
            print(f"   - {username}: {user_data['password']}")

        print(f"\nCreated {len(created_containers)} containers:")
        for number, cost in created_containers:
            print(f"   - {number}: ${cost:.2f}")

        print(f"\nTotal: {len(created_users)} users and {len(created_containers)} containers created!")

    except Exception as e:
        db.rollback()
        print(f" Error initializing database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
