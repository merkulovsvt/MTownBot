from fastapi import FastAPI
from sqladmin import Admin, ModelView

from bot.utils.database.models import engine, User, Lead

app = FastAPI()
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.chat_id]


class LeadAdmin(ModelView, model=Lead):
    pass


admin.add_view(UserAdmin)
admin.add_view(LeadAdmin)
