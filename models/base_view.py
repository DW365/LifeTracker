from flask_admin.contrib.mongoengine import ModelView
import flask_admin as admin
import flask_login as login

class BaseView(ModelView):
    list_template = 'list.html'
    action_disallowed_list = 'delete'
    create_modal = True
    edit_modal = True
    column_sortable_list = []

    def is_accessible(self):
        return login.current_user.is_authenticated

    def is_visible(self):
        return True
