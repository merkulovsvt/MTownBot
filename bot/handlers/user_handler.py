from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove

from bot.utils.bot.filters import NotURL, CLeadInProgress, MLeadInProgress
from bot.utils.bot.texts import start_text

router = Router()


# Хендлер для /start
@router.message(CommandStart(), ~MLeadInProgress())
async def command_start(message: types.Message):
    await message.answer(text=start_text,
                         disable_web_page_preview=True)


# Хендлер для остальных сообщений
@router.message(NotURL(), ~MLeadInProgress())
async def else_handler(message: types.Message):
    await message.reply(text="Это не ссылка на машину с mobile.de!",
                        reply_markup=ReplyKeyboardRemove())


# Хендлер для остальных сообщений
@router.callback_query(F.data == 'inactive')
async def inactive_handler(callback: types.CallbackQuery):
    await callback.answer()
