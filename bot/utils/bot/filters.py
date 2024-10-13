import os

import validators
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from bot.utils.database.requests import get_user_data

load_dotenv()


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return str(message.chat.id) == os.environ.get('ADMIN_CHAT_ID')


class MLeadInProgress(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return bool(await get_user_data(chat_id=message.chat.id, column_name='lead_id_in_progress'))


class CLeadInProgress(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return bool(await get_user_data(chat_id=callback.message.chat.id, column_name='lead_id_in_progress'))


class URL(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return validators.url(message.text) and 'mobile.de' in message.text


class NotURL(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not (validators.url(message.text) and 'mobile.de' in message.text)
