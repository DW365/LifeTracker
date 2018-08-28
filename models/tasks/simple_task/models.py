from markupsafe import Markup
from mongoengine import DateTimeField, ListField, ReferenceField

from models.category import TaskCategory
from models.tasks.base_task import BaseTask


class CategoryTask(BaseTask):
    categories = ListField(ReferenceField(TaskCategory))
    complete_day = DateTimeField()

    @property
    def date(self):
        raise NotImplemented()


class OneTimeTask(CategoryTask):
    complete_before = DateTimeField(required=True)

    @property
    def date(self):
        return Markup(f"До <b>{self.complete_before.strftime('%d.%m.%y')}</b>")


class ContinuousTask(CategoryTask):
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)

    @property
    def date(self):
        return Markup(f"С <b>{self.start_date.strftime('%d.%m.%y')}</b> до <b>{self.end_date.strftime('%d.%m.%y')}</b>")


