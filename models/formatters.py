from flask import url_for
from flask_admin.contrib.mongoengine import helpers
from flask_admin.helpers import get_url
from markupsafe import Markup


def bold_date(view, context, model, name):
    return Markup(f'<b>{model.date.strftime("%d.%m.%y")}</b>')


def icon(view, context, model, name):
    if model.icon:
        return Markup(
            f'<div class="image-thumbnail">'
            f'<img src="{view.get_url(".api_file_view", **helpers.make_thumb_args(model.icon))}"/>'
            f'</div>')


def big_icon(view, context, model, name):
    if model.icon:
        return Markup(
            f'<div class="image-thumbnail big">'
            f'<img src="{view.get_url(".api_file_view", **helpers.make_thumb_args(model.icon))}"/>'
            f'</div>')


def address(view, context, model, name):
    if model.icon:
        splitted = model.address.split("src")
        splitted.insert(1, 'width="300" height="250" src')
        return Markup(''.join(splitted))


def actions(view, context, model, name):
    return Markup(
        f'<a href="{get_url("incoming.create_view", url=url_for(".index_view"),modal=True,wallet=model.id)}" '
        f'data-target="#fa_modal_window" data-toggle="modal" class="btn btn-block btn-success">'
        f'<span class="glyphicon glyphicon-chevron-down"></span> Добавить доход</a>'

        f'<a href="{get_url("outcoming.create_view", url=url_for(".index_view"),modal=True,wallet=model.id)}" '
        f'data-target="#fa_modal_window" data-toggle="modal" class="btn btn-block btn-warning">'
        f'<span class="glyphicon glyphicon-chevron-up"></span> Добавить расход</a>')


def modify_status(view, context, model, name):
    if model.is_completed_today:
        return Markup(
            u'<a href="%s" class="btn btn-block btn-success"><span class="glyphicon glyphicon-ok"></span> Сделано</a>') % (
                   url_for('everyday_tasks.complete', id=model.id))
    else:
        return Markup(
            u'<a href="%s" class="btn btn-block btn-danger"><span class="glyphicon glyphicon-remove"></span> Не сделано</a>' % (
                url_for('everyday_tasks.complete', id=model.id))
        )
