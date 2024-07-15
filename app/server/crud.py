from sqlalchemy import select

from app.server.models import User
from app.server.schemas import UserModel


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def create_user(self, user: UserModel) -> UserModel:
        async with self.session() as session:
            user = User(username=user.user_name, hashed_password=user.hashed_password)
            session.add(user)
            await session.commit()

    async def get_all_users(self):
        async with self.session() as session:
            print(1)
            query = await session.execute(select(User))
            # print(query.scalars().all())
            print(query)


            return query.scalars().all()
