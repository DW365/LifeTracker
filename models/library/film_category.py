from flask_admin.contrib.mongoengine import ModelView
from mongoengine import *


class FilmCategory(Document):
    name = StringField(required=True, max_length=500)

    def __unicode__(self):
        return self.name


class FilmCategoryView(ModelView):
    list_template = 'list.html'
    action_disallowed_list = 'delete'
    column_labels = dict(name='Название')