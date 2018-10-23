from flask_admin import BaseView, expose
from mongoengine import Document, StringField
import flask_admin as admin
import flask_login as login
from flask_admin.contrib.mongoengine import ModelView

from models.Trip import Trip


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


class TripLogView(BaseView):
    @expose('/')
    def index(self):
        def get_color(trip):
            return {"ЛСД":"green",
                    "Амфетамин":"blue",
                    "Трава": "yellow"}[trip.description]
        return self.render('trip_log.html', trips=Trip.objects(), dates=[i.date for i in Trip.objects()], get_color=get_color)


    def is_accessible(self):
        return login.current_user.is_authenticated

    def is_visible(self):
        return True


class BaseView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def is_visible(self):
        return False
