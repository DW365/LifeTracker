from datetime import datetime

from flask_admin.contrib.mongoengine import ModelView
from mongoengine import *

from models.finances.base_operation import BaseOperation, BaseOperationView
from models.finances.incoming_category import IncomingCategory
from models.finances.outcoming_category import OutcomingCategory


class OutcomingOperation(BaseOperation):
    category = ListField(ReferenceField(OutcomingCategory))


class OutomingOperationView(BaseOperationView):
    pass