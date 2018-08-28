from markupsafe import Markup
from mongoengine import DateTimeField

from models.tasks.base_task import BaseTask, BaseTaskView


class HangingTask(BaseTask):
    started_at = DateTimeField(required=False)

    @property
    def date(self):
        if self.started_at:
            return Markup(f"От <b>{self.started_at.strftime('%d.%m.%y')}</b>")
        else:
            return ""


class HangingTaskView(BaseTaskView):
    column_list = ["description", "date"]

    def is_visible(self):
        return True