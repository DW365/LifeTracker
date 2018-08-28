from flask_admin.contrib.mongoengine import ModelView


class BaseView(ModelView):
    list_template = 'list.html'
    action_disallowed_list = 'delete'
    create_modal = True
    edit_modal = True
    column_sortable_list = []
