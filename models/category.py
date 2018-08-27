from mongoengine import *
from flask_admin.contrib.mongoengine import ModelView


class Category(Document):
    name = StringField(required=True, max_length=500)

    def __unicode__(self):
        return self.name

    meta = {'allow_inheritance': True}


class TaskCategory(Category):
    pass


class FilmCategory(Category):
    pass


class BookCategory(Category):
    pass


class IncomingCategory(Category):
    pass


class OutcomingCategory(Category):
    pass


class CategoryView(ModelView):
    list_template = 'list.html'
    action_disallowed_list = 'delete'
    column_labels = dict(name='Название')
