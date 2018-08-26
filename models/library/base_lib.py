from datetime import datetime

from flask import flash, request
from flask_admin import expose
from flask_admin.babel import gettext
from flask_admin.contrib.mongoengine import ModelView, form, helpers
from flask_admin.form import FormOpts
from flask_admin.helpers import get_redirect_target
from markupsafe import Markup
from mongoengine import *
from werkzeug.utils import redirect


class BaseLib(Document):
    icon = ImageField()
    name = StringField(required=True, max_length=400)
    description = StringField()
    review = StringField()
    completed = BooleanField(default=False)
    date = DateTimeField()
    meta = {'allow_inheritance': True}


def bold_date(view, context, model, name):
    return Markup(
        f'<b>{model.date.strftime("%d.%m.%y")}</b>'
    )


def icon(view, context, model, name):
    if model.icon:
        return Markup(
            ('<div class="image-thumbnail">' +
             '<img src="%(thumb)s"/>' +
             '</div>') %
            {
                'thumb': view.get_url('.api_file_view', **helpers.make_thumb_args(model.icon)),
            })


class BaseLibView(ModelView):
    action_disallowed_list = 'delete'
    list_template = 'list.html'
    column_labels = dict(description='Описание', date="Дата", price="Сумма", wallet='Кошелек', category="Жанр",icon="",name="Название",review="Комментарий")
    column_formatters = dict(icon=icon, date=bold_date)
    create_modal = True
    can_create = True
