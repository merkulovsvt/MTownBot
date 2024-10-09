from aiogram import Router, types
from aiogram.filters import Command

from bot.utils.bot.filters import IsAdmin
from bot.utils.bot.texts import start_text

router = Router()


# Хендлер для /editPercent
@router.message(Command('editPercent'), IsAdmin())
async def edit_percent(message: types.Message):
    await message.answer(text=start_text,
                         disable_web_page_preview=True)
    message.chat.full_name