from datetime import datetime
from flask import request, redirect
from flask_admin import expose
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from mongoengine import *
from flask_admin.contrib.mongoengine import ModelView
from models.category import TaskCategory
from models.formatters import modify_status


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
