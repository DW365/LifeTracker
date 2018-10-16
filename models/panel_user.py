from mongoengine import Document, StringField
import flask_admin as admin
import flask_login as login
from flask_admin.contrib.mongoengine import ModelView


class PanelUser(Document):
    login = StringField(max_length=80, unique=True)
    password = StringField(max_length=64)

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.login


class IndexView(admin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def is_visible(self):
        return False


class BaseView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def is_visible(self):
        return False
