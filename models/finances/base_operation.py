from datetime import datetime

from flask import flash, request
from flask_admin import expose
from flask_admin.babel import gettext
from flask_admin.contrib.mongoengine import ModelView, form
from flask_admin.form import FormOpts
from flask_admin.helpers import get_redirect_target
from markupsafe import Markup
from mongoengine import *
from werkzeug.utils import redirect


class BaseOperation(Document):
    description = StringField(required=True)
    price = FloatField(required=True)
    date = DateTimeField(required=True, default=datetime.now())
    wallet = ReferenceField("Wallet")
    meta = {'allow_inheritance': True}


def bold_date(view, context, model, name):
    return Markup(
            f'<b>{model.date.strftime("%d.%m.%y")}</b>'
        )


class BaseOperationView(ModelView):
    action_disallowed_list = 'delete'
    list_template = 'list.html'
    create_modal_template = 'admin/model/modals/create.html'
    column_list = ["description", "date", "price", "wallet", "category"]
    column_labels = dict(description='Описание', date="Дата", price="Сумма", wallet='Кошелек', category="Категория")
    column_formatters = dict(price=lambda v, c, m, p: f"{m.price} {m.wallet.currency}", date=bold_date)
    create_modal = True
    can_create = True

    def create_form(self, obj=None):
        form = super(BaseOperationView, self).create_form()
        # raise Exception
        if 'wallet' in request.args:
            from models.finances.wallet import Wallet
            form.wallet.data = Wallet.objects(id=request.args['wallet']).first()
        return form
