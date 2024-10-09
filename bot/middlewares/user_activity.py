from typing import Dict, Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.utils.database.requests import update_user_activity


class UserActivity(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        await update_user_activity(
            chat_id=event.message.chat.id if event.message else event.callback_query.message.chat.id,
            username=event.message.chat.username if event.message else event.callback_query.message.chat.username,
            name=event.message.chat.full_name if event.message else event.callback_query.message.chat.full_name)

        result = await handler(event, data)

        return result
