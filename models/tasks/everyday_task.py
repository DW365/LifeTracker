from datetime import datetime

from flask import request, redirect, url_for
from flask_admin import expose
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from markupsafe import Markup
from mongoengine import *
from flask_admin.contrib.mongoengine import ModelView

from models.tasks.task_category import TaskCategory


class EveryDayTask(Document):
    description = StringField(required=True)
    completed_on = ListField(DateTimeField(default=datetime.now(), required=True))
    active = BooleanField(default=True)
    categories = ListField(ReferenceField(TaskCategory))
    order = IntField()

    @property
    def is_completed_today(self):
        if self.completed_on:
            return self.completed_on[-1].day == datetime.today().day
        else:
            return False


def modify_status(view, context, model, name):
    if model.is_completed_today:
        return Markup(
            u'<a href="%s" class="btn btn-block btn-success"><span class="glyphicon glyphicon-ok"></span> Сделано</a>') % (
                url_for('everyday_tasks.complete', id=model.id))
    else:
        return Markup(
            u'<a href="%s" class="btn btn-block btn-danger"><span class="glyphicon glyphicon-remove"></span> Не сделано</a>' % (
                url_for('everyday_tasks.complete', id=model.id))
        )


class EveryDayTaskView(ModelView):
    list_template = 'list.html'
    details_modal_template = 'everyday_task_details.html'
    action_disallowed_list = 'delete'
    column_list = ["description", "is_completed_today"]
    column_formatters = dict(is_completed_today=modify_status)
    column_sortable_list = []
    column_labels = dict(description='Задача', categories ="Категория", is_completed_today='Статус')
    can_view_details = True
    edit_modal = True
    details_modal = True

    def is_visible(self):
            return True

    def get_query(self):
        return self.model.objects(active=True).order_by("order")

    @expose('/complete/', methods=('POST', 'GET'))
    def complete(self):
        return_url = get_redirect_target() or self.get_url('.index_view')
        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)
        model = self.get_one(id)
        if not model.is_completed_today:
            model.completed_on.append(datetime.now())
            model.save()
        elif model.completed_on:
                del model.completed_on[-1]
                model.save()
        return redirect(return_url)
