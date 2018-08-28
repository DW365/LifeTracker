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
    if (hasattr(model, 'is_completed_period') and model.is_completed_period) or model.is_completed:
        return Markup(
            u'<a href="%s" class="btn btn-block btn-success">'
            u'<span class="glyphicon glyphicon-ok">'
            u'</span> Сделано</a>') % (url_for('.complete', id=model.id))
    else:
        return Markup(
            u'<a href="%s" class="btn btn-block btn-danger">'
            u'<span class="glyphicon glyphicon-remove">'
            u'</span> Не сделано</a>' % (url_for('.complete', id=model.id)))


def mark_list(view, context, model, name):
    text = getattr(model, name)
    lines = text.split("\r\n")
    lines = map(lambda x: f"<li>{x}</li>", lines)
    return Markup(f"<ul>{''.join(lines)}</ul>")


def stars(view, context, model, name):
    return Markup('<span class="glyphicon glyphicon-star"></span>'*model.mark)
