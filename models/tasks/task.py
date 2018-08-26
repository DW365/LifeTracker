from datetime import datetime, timedelta

from flask import request, redirect, url_for
from flask_admin import expose
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from markupsafe import Markup
from mongoengine import *
from flask_admin.contrib.mongoengine import ModelView
from mongoengine.queryset.visitor import Q
from models.tasks.task_category import TaskCategory


class Task(Document):
    description = StringField(required=True)
    date = DateTimeField(default=datetime.now())
    end_date = DateTimeField()
    is_completed = BooleanField(default=False)
    categories = ListField(ReferenceField(TaskCategory))
    archived = BooleanField(default=False)


def modify_status(view, context, model, name):
    if model.is_completed:
        return Markup(
            u'<a href="%s" class="btn btn-block btn-success"><span class="glyphicon glyphicon-ok"></span> Сделано</a>') % (
                   url_for('tasks.complete', id=model.id, view=view.get_url('.index_view')))
    else:
        return Markup(
            u'<a href="%s" class="btn btn-block btn-danger"><span class="glyphicon glyphicon-remove"></span> Не сделано</a>' % (
                url_for('tasks.complete', id=model.id, view=view.get_url('.index_view')))
        )


def bold_date(view, context, model, name):
    if not model.end_date:
        return Markup(
            f'<b>{model.date.strftime("%d.%m.%y")}</b> в <b>{model.date.strftime("%H:%M")}</b>'
        )
    else:
        return Markup(
            f'с <b>{model.date.strftime("%d.%m.%y")}</b> до <b>{model.end_date.strftime("%d.%m.%y")}</b>'
        )


class TaskView(ModelView):
    # column_filters = ['date']
    column_list = ["description", "date", "categories", "is_completed"]
    column_default_sort = "date"
    list_template = 'list.html'
    action_disallowed_list = 'delete'
    column_labels = dict(description='Задача', date="Дата", categories="Категория", is_completed='Статус')
    column_formatters = dict(is_completed=modify_status, date=bold_date)

    def is_visible(self):
        return False

    def get_query(self):
        return self.model.objects()

    @expose('/complete/', methods=('POST', 'GET'))
    def complete(self):
        return_url = get_redirect_target() or self.get_url('.index_view')
        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)
        model = self.get_one(id)
        if not model.is_completed:
            model.is_completed = True
            model.save()
        else:
            model.is_completed = False
            model.save()
        view = get_mdict_item_or_list(request.args, 'view')
        if view:
            return_url = view

        return redirect(return_url)


class TodayTasksView(TaskView):
    column_default_sort = None

    def is_visible(self):
        return True

    def get_query(self):
        return self.model.objects(
            Q(date__lte=(datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0),
              end_date=None, archived__ne=False, is_completed=False)
            |
            Q(date__gte=datetime.now().replace(hour=0, minute=0, second=0),
              date__lte=(datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0),
              end_date=None, archived__ne=True)
            |
            Q(date__lte=datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1),
              end_date__gte=datetime.now().replace(hour=0, minute=0, second=0), is_completed=False)
        ).order_by('-is_completed', 'end_date','date')


class ActiveTasksView(TaskView):
    def is_visible(self):
        return True

    def get_query(self):
        return self.model.objects(Q(archived__ne=True, is_completed=False))


class ArchiveTasksView(TaskView):
    column_default_sort = "-date"

    def is_visible(self):
        return True

    def get_query(self):
        return self.model.objects(Q(archived=True) | Q(is_completed=True))
        # return self.model.objects(
        #     Q(archived=True) |
        #     Q(date__lte=(datetime.now()).replace(hour=0, minute=0, second=0), is_completed=True) |
        #     Q(date__lte=(datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0), is_completed=True, end_date__ne=None))
