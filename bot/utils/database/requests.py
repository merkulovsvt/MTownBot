from datetime import datetime

from sqlalchemy import select

from bot.utils.database.models import async_session, User, Lead


# User requests
async def update_user_activity(chat_id: int, username: str, name: str):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))

        user = result.scalars().first()

        if user:
            user.last_activity = datetime.now()
            user.notification_check = False
        else:
            new_user = User(chat_id=chat_id, name=name, username=username)
            session.add(new_user)
        await session.commit()


async def update_user(chat_id: int, **kwargs):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))
        user = result.scalars().first()

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        await session.commit()


async def get_user_data(chat_id: int, column_name: str):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id))
        user = result.scalars().first()

        # user_data = {key: getattr(user, key) for key in data}

        return getattr(user, column_name, None)


# Lead requests
async def create_lead(chat_id: int, username: str, car_name: str, url: str):
    async with async_session() as session:
        new_lead = Lead(user_chat_id=chat_id, username=username, car_name=car_name, url=url)
        session.add(new_lead)
        await session.flush()
        new_lead_id = new_lead.id
        await session.commit()
        return new_lead_id


async def get_lead_data(lead_id: int, column_name: str):
    async with async_session() as session:
        result = await session.execute(
            select(Lead).where(Lead.id == lead_id))
        lead = result.scalars().first()

        return getattr(lead, column_name, None)


async def update_lead(lead_id: int, **kwargs):
    async with async_session() as session:
        result = await session.execute(
            select(Lead).where(Lead.id == lead_id))
        lead = result.scalars().first()

        for key, value in kwargs.items():
            if hasattr(lead, key):
                setattr(lead, key, value)
        await session.commit()
