from mongoengine import ReferenceField

from models.category import BookCategory
from models.library.base_lib import BaseLib, BaseLibView


class Book(BaseLib):
    category = ReferenceField(BookCategory)


class BookView(BaseLibView):
    column_list = ["icon", "name", "category", "description"]

    def get_query(self):
        return self.model.objects(completed=False)


class ReadedBookView(BaseLibView):
    column_list = ["icon", "name", "category", "date", "review"]

    def get_query(self):
        return self.model.objects(completed=True)
