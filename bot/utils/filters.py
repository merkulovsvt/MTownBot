import validators
from aiogram.filters import BaseFilter
from aiogram.types.message import Message


class URL(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return validators.url(message.text) and 'mobile.de' in message.text


class NotURL(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not (validators.url(message.text) and 'mobile.de' in message.text)
