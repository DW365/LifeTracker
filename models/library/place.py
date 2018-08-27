from mongoengine import *
from models.category import FilmCategory
from models.formatters import big_icon, address
from models.library.base_lib import BaseLib, BaseLibView


class Place(BaseLib):
    address = StringField()


class PlaceView(BaseLibView):
    column_list = ["icon", "name", "description", "address"]
    column_formatters = dict(icon=big_icon, address=address)

    def get_query(self):
        return self.model.objects(completed=False)


class VisitedPlaceView(BaseLibView):
    column_list = ["icon", "name", "category", "date", "review"]
    column_formatters = dict(icon=big_icon)

    def get_query(self):
        return self.model.objects(completed=True)
