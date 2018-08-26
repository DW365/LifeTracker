from datetime import datetime, timedelta

from flask import request, redirect, url_for
from flask_admin import expose
from flask_admin.helpers import get_redirect_target, get_url
from flask_admin.model.helpers import get_mdict_item_or_list
from markupsafe import Markup
from mongoengine import *
from flask_admin.contrib.mongoengine import ModelView


class TaskCategory(Document):
    name = StringField(required=True, max_length=500)

    def __unicode__(self):
        return self.name


class TaskCategoryView(ModelView):
    list_template = 'list.html'
    action_disallowed_list = 'delete'
    column_labels = dict(name='Название')
