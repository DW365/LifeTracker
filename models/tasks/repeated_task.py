from datetime import datetime

from flask import request, redirect
from flask_admin import expose
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from mongoengine import ListField, DateTimeField, IntField

from models.formatters import modify_status
from models.tasks.base_task import BaseTask, BaseTaskView


class RepeatedTask(BaseTask):
    completed_on = ListField(DateTimeField(default=datetime.now(), required=True))
    order = IntField()
    period = None

    @property
    def is_completed_period(self):
        if self.completed_on:
            return self.completed_on[-1].day >= datetime.now().day - self.period + 1
        else:
            return False


class EverydayTask(RepeatedTask):
    period = 1


class EveryWeekTask(RepeatedTask):
    period = 7


class EveryMonthTask(RepeatedTask):
    period = 30


class RepeatedTaskView(BaseTaskView):
    details_modal_template = 'everyday_task_details.html'
    column_exclude_list = ['archive', 'order', '_cls', 'is_completed']
    form_excluded_columns = ['is_completed']
    column_formatters = dict(completed_on=modify_status)
    column_sortable_list = []
    can_view_details = True

    def is_visible(self):
        return True

    def get_query(self):
        return self.model.objects(archive__ne=True).order_by("order")

    @expose('/complete/', methods=('POST', 'GET'))
    def complete(self):
        return_url = get_redirect_target() or self.get_url('.index_view')
        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)
        model = self.get_one(id)
        if not model.is_completed_period:
            model.completed_on.append(datetime.now())
            model.save()
        elif model.completed_on:
            del model.completed_on[-1]
            model.save()
        return redirect(return_url)