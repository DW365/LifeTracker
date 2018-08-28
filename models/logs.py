from datetime import datetime

from mongoengine import *

from models.base_view import BaseView
from models.formatters import bold_date, mark_list, stars


class BaseLog(Document):
    comment = StringField()
    positive = StringField()
    negative = StringField()
    mark = IntField(choices=[1, 2, 3, 4, 5])
    date = DateTimeField(default=datetime.now())
    meta = {'allow_inheritance': True}


class DayLog(BaseLog):
    hours0 = ListField(StringField(max_length=100))
    hours1 = ListField(StringField(max_length=100))
    hours2 = ListField(StringField(max_length=100))
    hours3 = ListField(StringField(max_length=100))
    hours4 = ListField(StringField(max_length=100))
    hours5 = ListField(StringField(max_length=100))
    hours6 = ListField(StringField(max_length=100))
    hours7 = ListField(StringField(max_length=100))


class DayLogView(BaseView):
    column_list = ["date", "comment", "positive", "negative", "mark"]
    column_formatters = dict(date=bold_date, positive=mark_list, negative=mark_list, mark=stars)
    column_labels = dict(date="Дата", comment="Комментарий", positive="Плюсы", negative="Минусы", mark="Оценка")
    form_args = dict(
        hours0=dict(label='С 00:00 до 03:00'),
        hours1=dict(label='С 03:00 до 06:00'),
        hours2=dict(label='С 06:00 до 08:00'),
        hours3=dict(label='С 09:00 до 12:00'),
        hours4=dict(label='С 12:00 до 15:00'),
        hours5=dict(label='С 15:00 до 18:00'),
        hours6=dict(label='С 18:00 до 21:00'),
        hours7=dict(label='С 21:00 до 00:00'),
    )
