from flask import url_for
from flask_admin.contrib.mongoengine import ModelView, helpers
from flask_admin.helpers import get_url
from markupsafe import Markup
from mongoengine import *

from models.finances.base_operation import BaseOperation
from models.finances.incoming import IncomingOperation
from models.finances.outcoming import OutcomingOperation


class Wallet(Document):
    name = StringField(required=True, max_length=500)
    requisites = StringField(max_length=500)
    currency = StringField(max_length=3, default="RUR")
    icon = ImageField()

    def __unicode__(self):
        return self.name

    @property
    def balance(self):
        return IncomingOperation.objects(wallet=self).sum("price")-OutcomingOperation.objects(wallet=self).sum("price")

    # def balance_at_date(self, date):
    #     return 0 + IncomingOperation.objects(wallet=self, date_lte=date).sum("price")-OutcomingOperation.objects(wallet=self, date_lte=date).sum("price")

    @property
    def dates_balance(self):
        dates = {}
        last_value = 0
        # raise Exception()
        for o in BaseOperation.objects(wallet=self).order_by("date"):
            date = o.date.strftime("%Y-%m-%d")
            last_value += o.price if isinstance(o, IncomingOperation) else -o.price
            if date not in dates:
                dates[date] = last_value
            else:
                dates[date] = last_value
        return dates


def icon(view, context, model, name):
    if model.icon:
        return Markup(
            ('<div class="image-thumbnail">' +
             '<img src="%(thumb)s"/>' +
             '</div>') %
            {
                'thumb': view.get_url('.api_file_view', **helpers.make_thumb_args(model.icon)),
            })

def actions(view, context, model, name):
        return Markup(f'<a href="{get_url("incoming.create_view", url=url_for(".index_view"),modal=True,wallet=model.id)}" data-target="#fa_modal_window" data-toggle="modal" class="btn btn-block btn-success"><span class="glyphicon glyphicon-chevron-down"></span> Добавить доход</a>'
                      f'<a href="{get_url("outcoming.create_view", url=url_for(".index_view"),modal=True,wallet=model.id)}" data-target="#fa_modal_window" data-toggle="modal" class="btn btn-block btn-warning"><span class="glyphicon glyphicon-chevron-up"></span> Добавить расход</a>')


class WalletView(ModelView):
    list_template = 'list.html'
    column_list = ["icon","name","requisites", "balance", "actions"]
    action_disallowed_list = 'delete'
    column_labels = dict(name='Название', icon="",requisites="Реквизиты", balance="Баланс", actions="Действия")
    column_formatters = dict(icon=icon, balance=lambda v, c, m, p: f"{m.balance} {m.currency}", actions=actions)
    edit_modal = True
    can_view_details = True
    details_template = "wallet_details.html"
