from mongoengine import *
from models.category import OutcomingCategory
from models.finances.operations.base_operation import BaseOperation, BaseOperationView


class OutcomingOperation(BaseOperation):
    category = ListField(ReferenceField(OutcomingCategory))


class OutomingOperationView(BaseOperationView):
    pass
