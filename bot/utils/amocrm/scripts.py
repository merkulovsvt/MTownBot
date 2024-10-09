import asyncio

from amocrm.v2 import Lead as Lead_, Contact as Contact_
from amocrm.v2.entity import custom_field

from bot.utils.database.requests import get_user_data, update_user


class Lead(Lead_):
    car_url = custom_field.TextCustomField(name='Ссылка на авто', field_id=3014139)


class Contact(Contact_):
    tg_username = custom_field.TextCustomField(name='Telegram username', field_id=3014153)
    phone = custom_field.TextCustomField(name='Телефон')


async def upload_lead(chat_id: int, car_url: str, tg_username: str, name: str, phone: str) -> bool:
    try:

        contact_id = await get_user_data(chat_id=chat_id, column_name='contact_id')
        if contact_id:
            contact = Contact.objects.get(object_id=contact_id)
        else:
            contact = Contact(name=name, phone=phone, tg_username='@' + tg_username)
            await asyncio.to_thread(contact.save)
            await update_user(chat_id=chat_id, contact_id=contact.id)

        lead = Lead(car_url=car_url)
        await asyncio.to_thread(lead.save)
        await asyncio.to_thread(lead.contacts.append, contact, False)

        return True
    except Exception as e:
        print(e)
        return False
