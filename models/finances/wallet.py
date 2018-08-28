from flask_admin.contrib.mongoengine import ModelView
from mongoengine import *

from models.base_view import BaseView
from models.finances.operations.base_operation import BaseOperation
from models.formatters import icon, actions
from models.finances.operations.incoming import IncomingOperation
from models.finances.operations.outcoming import OutcomingOperation


class Wallet(Document):
    name = StringField(required=True, max_length=500)
    requisites = StringField(max_length=500)
    currency = StringField(max_length=3, default="RUR")
    icon = ImageField()

    def __unicode__(self):
        return self.name

    @property
    def balance(self):
        return IncomingOperation.objects(wallet=self).sum("price") - \
               OutcomingOperation.objects(wallet=self).sum("price")

    @property
    def dates_balance(self):
        dates = {}
        last_value = 0
        for o in BaseOperation.objects(wallet=self).order_by("date"):
            date = o.date.strftime("%Y-%m-%d")
            last_value += o.price if isinstance(o, IncomingOperation) else -o.price
            if date not in dates:
                dates[date] = last_value
            else:
                dates[date] = last_value
        return dates


class WalletView(BaseView):
    column_list = ["icon", "name", "requisites", "balance", "actions"]
    column_labels = dict(name='Название', icon="", requisites="Реквизиты", balance="Баланс", actions="Действия")
    column_formatters = dict(icon=icon, balance=lambda v, c, m, p: f"{m.balance} {m.currency}", actions=actions)
    edit_modal = True
    can_view_details = True
    details_template = "wallet_details.html"
