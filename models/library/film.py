from mongoengine import ReferenceField
from models.category import FilmCategory
from models.library.base_lib import BaseLib, BaseLibView


class Film(BaseLib):
    category = ReferenceField(FilmCategory)


class FilmView(BaseLibView):
    column_list = ["icon", "name", "category", "description"]

    def get_query(self):
        return self.model.objects(completed=False)


class WatchedFilmView(BaseLibView):
    column_list = ["icon", "name", "category", "date", "review"]

    def get_query(self):
        return self.model.objects(completed=True)
