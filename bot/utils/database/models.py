from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, DateTime, BIGINT, ForeignKey, Enum
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship

from bot.utils.bot.scripts import BASE_DIR

load_dotenv()

engine = create_async_engine(f"sqlite+aiosqlite:///{BASE_DIR}/DataBase.db")
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BIGINT, unique=True)

    username = Column(String)
    name = Column(String)
    phone = Column(String, unique=True)

    contact_id = Column(Integer)
    lead_id_in_progress = Column(Integer, default=None)

    created_at = Column(DateTime, default=datetime.now())
    last_activity = Column(DateTime, default=datetime.now())


class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True)
    user_chat_id = Column(BIGINT, ForeignKey('users.chat_id'), nullable=False)

    message_id = Column(BIGINT)

    status = Column(Enum('created', 'canceled', 'uploaded', name='lead_status'),
                    nullable=False, default="created")

    price = Column(String)
    price_type = Column(String)

    car_name = Column(String)
    url = Column(String)

    created_at = Column(DateTime, default=datetime.now())
    canceled_at = Column(DateTime, default=None)
    uploaded_at = Column(DateTime, default=None)

    user = relationship("User", backref="requests")


async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
