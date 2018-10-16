import flask_admin as admin
from flask import Flask, request, session, render_template, redirect
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.menu import MenuLink
from flask_babelex import Babel
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

import flask_admin as admin
import flask_login as login
from config import HOST, PORT, USERNAME, PASSWORD, DB_NAME
from models.category import CategoryView, FilmCategory, BookCategory, OutcomingCategory, IncomingCategory, TaskCategory
from models.finances.operations.incoming import IncomingOperation, IncomingOperationView
from models.finances.operations.outcoming import OutomingOperationView, OutcomingOperation
from models.finances.wallet import WalletView, Wallet
from models.library.book import Book, BookView, ReadedBookView
from models.library.film import FilmView, Film, WatchedFilmView
from models.library.place import Place, VisitedPlaceView, PlaceView
from models.logs import DayLog, DayLogView
from models.tasks.base_task import BaseTask, BaseTaskView
from models.tasks.hanging_task import HangingTask, HangingTaskView
from models.tasks.repeated_task import EverydayTask, EveryWeekTask, RepeatedTaskView
from models.tasks.simple_task.models import OneTimeTask, ContinuousTask, CategoryTask
from models.tasks.simple_task.views import OneTimeTaskView, ContinuousTaskView, TodayTaskView, \
    ActiveTaskView, ArchiveTaskView, WeekTaskView
from models.panel_user import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tNc4a7FsdHSvM78kMU'
app.config['MONGODB_SETTINGS'] = {'db': DB_NAME,
                                  'host': HOST,
                                  'port': PORT,
                                  'username': USERNAME,
                                  'password': PASSWORD}

login_manager = LoginManager()
login_manager.init_app(app)

babel = Babel(app)


@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'ru')


db = MongoEngine()
db.init_app(app)


def add_divider(a, cat):
    a.add_menu_item(MenuLink("", url="#", class_name="divider"), target_category=cat)


def add_tasks_menu(a, cat="Дела"):
    a.add_view(ContinuousTaskView(ContinuousTask))
    a.add_view(OneTimeTaskView(OneTimeTask))

    a.add_view(TodayTaskView(CategoryTask, name="На сегодня", endpoint="today_tasks", category=cat))
    a.add_view(WeekTaskView(CategoryTask, name="На неделю", endpoint="week_tasks", category=cat))
    a.add_view(ActiveTaskView(CategoryTask, name="Предстоящие", endpoint="active_tasks", category=cat))
    a.add_view(ArchiveTaskView(CategoryTask, name="Архив", endpoint="archive_tasks", category=cat))
    add_divider(a, cat)
    a.add_view(RepeatedTaskView(EverydayTask, name="Ежедневные", endpoint="everyday_tasks", category=cat))
    a.add_view(RepeatedTaskView(EveryWeekTask, name="Еженедельные", endpoint="everyweek_tasks", category=cat))
    # a.add_view(RepeatedTaskView(EveryMonthTask, name="Ежемесячные", endpoint="everymonth_tasks", category=cat))
    add_divider(a, cat)
    a.add_view(HangingTaskView(HangingTask, name="Подвешенные", endpoint="hanging_tasks", category=cat))
    a.add_view(BaseTaskView(BaseTask, name="Все дела", endpoint="tasks"))


def add_finances_menu(a, cat="Финансы"):
    a.add_view(IncomingOperationView(IncomingOperation, name="Доходы", endpoint="incoming", category=cat))
    a.add_view(OutomingOperationView(OutcomingOperation, name="Расходы", endpoint="outcoming", category=cat))
    add_divider(a, cat)
    a.add_view(WalletView(Wallet, name="Кошельки", endpoint="wallets", category=cat))


def add_settings_menu(a, cat="Настройки"):
    admin.add_view(CategoryView(TaskCategory, name="Категории дел", endpoint="tasks_cat", category=cat))
    add_divider(a, cat)
    admin.add_view(CategoryView(IncomingCategory, name="Категории доходов", endpoint="incoming_cat", category=cat))
    admin.add_view(CategoryView(OutcomingCategory, name="Категории расходов", endpoint="outcoming_cat", category=cat))
    add_divider(a, cat)
    admin.add_view(CategoryView(BookCategory, name="Жанры книг", endpoint="book_cat", category=cat))
    admin.add_view(CategoryView(FilmCategory, name="Жанры фильмов", endpoint="film_cat", category=cat))


def add_lib_menu(a, cat="Библиотека"):
    admin.add_view(BookView(Book, name="Книги", endpoint="books", category=cat))
    admin.add_view(ReadedBookView(Book, name="Прочитанные книги", endpoint="readed_books", category=cat))
    add_divider(a, cat)
    admin.add_view(FilmView(Film, name="Фильмы", endpoint="films", category=cat))
    admin.add_view(WatchedFilmView(Film, name="Просмотренные фильмы", endpoint="watched_films", category=cat))
    add_divider(a, cat)
    admin.add_view(PlaceView(Place, name="Места", endpoint="places", category=cat))
    admin.add_view(VisitedPlaceView(Place, name="Посещенные места", endpoint="visited_places", category=cat))


def add_logs_menu(a, cat="Логи"):
    admin.add_view(DayLogView(DayLog, name="За день", endpoint="daily", category=cat))
    admin.add_view(ModelView(Book, name="За неделю", endpoint="weekly", category=cat))
    admin.add_view(ModelView(Film, name="За месяц", endpoint="monthly", category=cat))


@app.route('/', methods=('GET', 'POST'))
def login_view():
    if request.method == 'POST':
        if not PanelUser.objects().first():
            PanelUser(login="admin", password="xk2987cdf").save()
        user = PanelUser.objects(login=request.form['login']).first()
        if user and user.password == request.form['password']:
            login.login_user(user)
            return redirect('/admin')
        else:
            return redirect("/")

    return render_template('form.html')


@login_manager.user_loader
def load_user(user_id):
    return PanelUser.objects(id=user_id).first()


if __name__ == '__main__':
    admin = admin.Admin(app, 'LIFE', base_template='layout.html', template_mode='bootstrap3',
                        index_view=IndexView(name=''))
    add_tasks_menu(admin)
    add_finances_menu(admin)
    add_lib_menu(admin)
    add_logs_menu(admin)
    add_settings_menu(admin)

    # admin.add_link(MenuLink(name='Мониторинг',
    #                         url='https://cloud.mongodb.com/freemonitoring/cluster/O5NUV2ZFXFRRNR45CTGEJJDIGSMF4K7J'))
    admin.add_link(MenuLink(name='Jupyter',
                            url='http://37.230.115.227:8888/'))

    app.run(host="0.0.0.0", debug=True, use_reloader=True, port=80)
