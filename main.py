import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from amocrm.v2 import tokens
from dotenv import load_dotenv

from bot.handlers import user_handler, parser_handler, lead_handler
from bot.middlewares.user_activity import UserActivity
from bot.utils.bot.scripts import stop_bot, start_bot
from bot.utils.database.models import start_db

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    await start_db()

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(user_handler.router, parser_handler.router, lead_handler.router)

    dp.update.outer_middleware(UserActivity())

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    tokens.default_token_manager(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        subdomain=os.getenv('SUBDOMAIN'),
        redirect_url=os.getenv('REDIRECT_URL'),
        storage=tokens.FileTokensStorage('tokens'),
    )

    tokens.default_token_manager.init(code=os.getenv('SECRET'), skip_error=False)
    asyncio.run(main())
