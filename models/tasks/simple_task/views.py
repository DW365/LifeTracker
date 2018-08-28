from flask import request, redirect
from flask_admin import expose
from flask_admin.helpers import get_url
from flask_admin.model.helpers import get_mdict_item_or_list
from mongoengine import Q

from models.formatters import modify_status
from models.tasks.base_task import BaseTaskView
from models.tasks.simple_task.models import OneTimeTask
from models.tools import tomorrow, today, next_week


class SimpleTaskView(BaseTaskView):
    column_sortable_list = []
    column_list = ["description", "date", "categories", "is_completed"]
    column_formatters = dict(is_completed=modify_status)
    create_modal = True
    edit_modal = True
    list_template = 'task_list.html'

    def is_visible(self):
        return True

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        id = get_mdict_item_or_list(request.args, 'id')
        if OneTimeTask.objects(id=id).first():
            return redirect(get_url('onetimetask.edit_view', **request.args))
        else:
            return redirect(get_url('continuoustask.edit_view', **request.args))


class SimpleTaskViewHided(SimpleTaskView):
    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        return super(BaseTaskView, self).edit_view()

    def is_visible(self):
        return False


class OneTimeTaskView(SimpleTaskViewHided):
    pass


class ContinuousTaskView(SimpleTaskViewHided):
    pass


class TodayTaskView(SimpleTaskView):
    def get_query(self):
        return self.model.objects((Q(_cls="BaseTask.CategoryTask.OneTimeTask",
                                     complete_before__lte=tomorrow()) |
                                   Q(_cls="BaseTask.CategoryTask.ContinuousTask",
                                     start_date__lte=tomorrow(),
                                     end_date__gte=today())) & (
                                      Q(archive__ne=True, is_completed=False))) \
            .order_by('-_cls', 'complete_before', 'end_date')


class WeekTaskView(SimpleTaskView):
    def get_query(self):
        return self.model.objects((Q(_cls="BaseTask.CategoryTask.OneTimeTask",
                                     complete_before__lte=next_week(),
                                     is_completed=False) |
                                   Q(_cls="BaseTask.CategoryTask.ContinuousTask",
                                     start_date__lte=next_week(),
                                     end_date__gte=today())) & (
                                      Q(archive__ne=True))) \
            .order_by('-_cls', 'complete_before', 'end_date')


class ActiveTaskView(SimpleTaskView):
    def get_query(self):
        return self.model.objects(is_completed=False, archive__ne=True).order_by('-_cls', 'complete_before', 'end_date')


class ArchiveTaskView(SimpleTaskView):
    def get_query(self):
        return self.model.objects(Q(archive=True) | Q(is_completed=True)).order_by('-complete_day')