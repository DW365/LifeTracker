from datetime import datetime

from flask_admin.contrib.mongoengine import ModelView
from mongoengine import *

from models.finances.base_operation import BaseOperation, BaseOperationView
from models.finances.incoming_category import IncomingCategory


class IncomingOperation(BaseOperation):
    category = ListField(ReferenceField(IncomingCategory))

class IncomingOperationView(BaseOperationView):
    pass