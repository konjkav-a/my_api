from .models import User
from .schemas import UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import generate_passwd_hash
from sqlalchemy import select


class UserService:
    async def get_user_by_email(self, email: str , session: AsyncSession):
        # SELECT * FROM user WHERE email = 'a@mail.com';
        statement = select(User).where(User.email == email) # type: ignore
        result = await session.exec(statement)
        user = result.scalar()  # return orm object

        return user

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    """
    user_data: UserCreateModel means:I expect user_data to be an instance of UserCreateModel.
    """
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        """
            Pydantic gives you the method:
            user_data.model_dump()
            This converts the Pydantic model into a plain dictionary of its fields.
        """
        user_data_dict = user_data.model_dump()

        """
        new_user = User(**user_data_dict) is == 
        new_user = User(email=user_data.email,username=user_data.username,password=user_data.password
        """
        new_user = User(**user_data_dict)

        new_user.password_hash = generate_passwd_hash(user_data_dict['password'])

        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)
        return new_user