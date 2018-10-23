from datetime import datetime

from mongoengine import *
from models.category import FilmCategory
from models.formatters import big_icon, address
from models.library.base_lib import BaseLib, BaseLibView


class Trip(Document):
    date = DateTimeField(required=True, default=datetime.now)
    description = StringField(required=True)

    meta = {"strict":False}


class TripView(BaseLibView):
    pass
    # column_list = ["icon", "name", "description", "address"]
    # column_formatters = dict(icon=big_icon, address=address)
    #
    # def get_query(self):
    #     return self.model.objects(completed=False)
