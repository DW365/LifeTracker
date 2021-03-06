from flask_admin.contrib.mongoengine import ModelView
from mongoengine import *

from models.base_view import BaseView
from models.formatters import bold_date, icon, address


class BaseLib(Document):
    icon = ImageField()
    name = StringField(required=True, max_length=400)
    description = StringField()
    review = StringField()
    completed = BooleanField(default=False)
    date = DateTimeField()
    meta = {'allow_inheritance': True}


class BaseLibView(BaseView):
    column_labels = dict(description='Описание', date="Дата", price="Сумма", wallet='Кошелек',
                         category="Жанр", icon="", name="Название", review="Комментарий", address="Адрес")
    column_formatters = dict(icon=icon, date=bold_date)
    create_modal = True
    can_create = True
