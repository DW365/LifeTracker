from mongoengine import *
from models.category import IncomingCategory
from models.finances.operations.base_operation import BaseOperation, BaseOperationView


class IncomingOperation(BaseOperation):
    category = ListField(ReferenceField(IncomingCategory))


class IncomingOperationView(BaseOperationView):
    pass
