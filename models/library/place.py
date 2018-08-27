from mongoengine import *
from models.category import FilmCategory
from models.library.base_lib import BaseLib, BaseLibView


class Place(BaseLib):
    address = StringField()
    location = GeoPointField()


class PlaceView(BaseLibView):
    # column_list = ["icon", "name", "category", "description"]

    def get_query(self):
        return self.model.objects(completed=False)


class VisitedPlaceView(BaseLibView):
    column_list = ["icon", "name", "category", "date", "review"]

    def get_query(self):
        return self.model.objects(completed=True)
