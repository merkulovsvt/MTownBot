from datetime import datetime

from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove

from bot.callbacks.lead_callbacks import LeadStartUpload, RetrySearch
from bot.keyboards.lead_keyboards import inline_lead_canceled, inline_lead_in_progress, reply_lead_in_progress, \
    inline_lead_uploaded
from bot.utils.amocrm.scripts import upload_lead
from bot.utils.bot.filters import MLeadInProgress
from bot.utils.database.requests import update_lead, update_user, get_user_data, get_lead_data

router = Router()


# Хендлер для повторного запроса
@router.callback_query(RetrySearch.filter())
async def retry_search_handler(callback: types.CallbackQuery, callback_data: RetrySearch):
    lead_id = callback_data.lead_id

    reply_markup = inline_lead_canceled()
    await callback.message.edit_reply_markup(reply_markup=reply_markup)

    await callback.message.answer(text='Отправьте мне ссылку на автомобиль с mobile.de/ru!',
                                  disable_web_page_preview=True)

    await update_lead(lead_id=lead_id, status='canceled', canceled_at=datetime.now())

    await callback.answer()


# Хендлер для старта отправки сделки
@router.callback_query(LeadStartUpload.filter())
async def lead_upload_begin_handler(callback: types.CallbackQuery, callback_data: LeadStartUpload):
    lead_id = callback_data.lead_id

    user_phone = await get_user_data(chat_id=callback.message.chat.id, column_name='phone')

    if user_phone:
        url = await get_lead_data(lead_id=lead_id, column_name='url')

        await upload_lead(callback.message.chat.id,
                          url,
                          callback.message.chat.username,
                          callback.message.chat.full_name,
                          user_phone)

        reply_markup = inline_lead_uploaded()
        message_id = await get_lead_data(lead_id=lead_id, column_name='message_id')
        await callback.message.bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                                             message_id=message_id,
                                                             reply_markup=reply_markup)

        await callback.message.answer(text='Поздравляю, заявка отправлена! В ближайшее время с вами свяжутся',
                                      reply_markup=ReplyKeyboardRemove())
        await callback.message.answer(text='Если хотите ещё - отправьте мне ссылку на автомобиль с mobile.de/ru!',
                                      disable_web_page_preview=True)

        await update_user(chat_id=callback.message.chat.id, lead_id_in_progress=None)
        await update_lead(lead_id=lead_id, status='uploaded', uploaded_at=datetime.now())
    else:
        reply_markup = inline_lead_in_progress()
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

        text, reply_markup = reply_lead_in_progress()
        await callback.message.answer(text=text, reply_markup=reply_markup)

        await update_user(chat_id=callback.message.chat.id, lead_id_in_progress=lead_id)

    await callback.answer()


# Хендлер для обработки номера телефона
@router.message(MLeadInProgress(), F.contact)
async def lead_upload_phone_handler(message: types.Message):
    user_phone = message.contact.phone_number

    await update_user(chat_id=message.chat.id, phone=user_phone)

    lead_id = await get_user_data(chat_id=message.chat.id, column_name='lead_id_in_progress')

    url = await get_lead_data(lead_id=lead_id, column_name='url')

    result = await upload_lead(message.chat.id,
                               url,
                               message.chat.username,
                               message.chat.full_name,
                               user_phone)
    if result:
        reply_markup = inline_lead_uploaded()
        message_id = await get_lead_data(lead_id=lead_id, column_name='message_id')
        await message.bot.edit_message_reply_markup(chat_id=message.chat.id,
                                                    message_id=message_id,
                                                    reply_markup=reply_markup)

        await message.answer(text='Поздравляю, заявка отправлена! В ближайшее время с вами свяжутся',
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(text='Если хотите ещё - отправьте мне ссылку на автомобиль с mobile.de/ru!',
                             disable_web_page_preview=True)

        await update_user(chat_id=message.chat.id, lead_id_in_progress=None)
        await update_lead(lead_id=lead_id, status='uploaded', uploaded_at=datetime.now())
    else:
        reply_markup = inline_lead_canceled()
        message_id = await get_lead_data(lead_id=lead_id, column_name='message_id')
        await message.bot.edit_message_reply_markup(chat_id=message.chat.id,
                                                    message_id=message_id,
                                                    reply_markup=reply_markup)
        await message.answer(text='Что-то не так, попробуйте отправить заявку снова!')

        await update_lead(lead_id=lead_id, status='canceled', canceled_at=datetime.now())
        await update_user(chat_id=message.chat.id, lead_id_in_progress=None)


# Хендлер для обработки НЕ номера телефона
@router.message(MLeadInProgress(), ~F.contact)
async def lead_upload_not_phone_handler(message: types.Message):
    if message.text == '❌ Отменить заявку':
        lead_id = await get_user_data(chat_id=message.chat.id, column_name='lead_id_in_progress')

        reply_markup = inline_lead_canceled()
        message_id = await get_lead_data(lead_id=lead_id, column_name='message_id')
        await message.bot.edit_message_reply_markup(chat_id=message.chat.id,
                                                    message_id=message_id,
                                                    reply_markup=reply_markup)

        await message.answer(text='Заявка отменена!', reply_markup=ReplyKeyboardRemove())
        await message.answer(text='Отправьте мне ссылку на автомобиль с mobile.de/ru!',
                             disable_web_page_preview=True)

        await update_lead(lead_id=lead_id, status='canceled', canceled_at=datetime.now())
        await update_user(chat_id=message.chat.id, lead_id_in_progress=None)

    else:
        text = 'Поделитесь контактом или отмените заявку!'
        _, reply_markup = reply_lead_in_progress()
        await message.answer(text=text, reply_markup=reply_markup)
