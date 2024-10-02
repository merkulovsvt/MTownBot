from aiogram import Router, types, F
from aiogram.filters import CommandStart

from bot.utils.filters import NotURL
from bot.utils.texts import start_text

router = Router()


# Хендлер для /start
@router.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer(text=start_text,
                         disable_web_page_preview=True)

    # bot.send_message(chat_id=message.chat.id,
    #                  text="Пришлите мне ссылку на машину с mobile.de и я выведу расчетную стоимость!")


# Хендлер для остальных сообщений
@router.message(NotURL(), F.text)
async def else_handler(message: types.Message):
    await message.reply(text="Это не ссылка на машину с mobile.de!")
