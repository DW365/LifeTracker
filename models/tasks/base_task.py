from datetime import datetime

from flask import request
from flask_admin import expose
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from mongoengine import *
from werkzeug.utils import redirect

from models.base_view import BaseView


class BaseTask(Document):
    description = StringField(required=True)
    is_completed = BooleanField(default=False)
    archive = BooleanField(default=False)

    meta = {'allow_inheritance': True}


class BaseTaskView(BaseView):
    column_labels = dict(description='Задача', date="Дата", categories="Категория", is_completed='Статус',
                         completed_on="Статус")

    def is_visible(self):
        return False

    @expose('/complete/', methods=('POST', 'GET'))
    def complete(self):
        return_url = get_redirect_target() or self.get_url('.index_view')
        mid = get_mdict_item_or_list(request.args, 'id')
        if mid is None:
            return redirect(return_url)
        model = self.get_one(mid)
        if not model.is_completed:
            model.is_completed = True
            model.complete_day = datetime.now()
            model.save()
        else:
            model.is_completed = False
            model.save()
        view = get_mdict_item_or_list(request.args, 'view')
        if view:
            return_url = view

        return redirect(return_url)


