from datetime import datetime

from flask import request, redirect, url_for
from flask_admin import expose
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from markupsafe import Markup
from mongoengine import *
from flask_admin.contrib.mongoengine import ModelView

from models.tasks.task_category import TaskCategory


class HangingTask(Document):
    description = StringField(required=True)
    completed = BooleanField(default=False)
    started_at = DateTimeField(default=datetime.now())
    categories = ListField(ReferenceField(TaskCategory))


def modify_status(view, context, model, name):
    if model.completed:
        return Markup(
            u'<a href="%s" class="btn btn-block btn-success"><span class="glyphicon glyphicon-ok"></span>Завершено</a>') % (
                url_for('hanging_tasks.complete', id=model.id))
    else:
        return Markup(
            u'<a href="%s" class="btn btn-block btn-danger"><span class="glyphicon glyphicon-remove"></span> Не завершено</a>' % (
                url_for('hanging_tasks.complete', id=model.id))
        )


class HangingTaskView(ModelView):
    list_template = 'list.html'
    column_list = ["description", "categories", "completed"]
    column_formatters = dict(completed=modify_status)
    action_disallowed_list = 'delete'
    column_labels = dict(description='Задача', categories ="Категория", completed='Статус')
    column_default_sort = "completed"

    def get_query(self):
        return self.model.objects()

    @expose('/complete/', methods=('POST', 'GET'))
    def complete(self):
        return_url = get_redirect_target() or self.get_url('.index_view')
        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)
        model = self.get_one(id)
        if not model.completed:
            model.completed = True
            model.save()
        else:
                model.completed=False;
                model.save()
        return redirect(return_url)
