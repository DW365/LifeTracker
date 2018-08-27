from flask import Flask, request, session
import flask_admin as admin
from flask_admin.menu import MenuLink
from flask_mongoengine import MongoEngine
from flask_babelex import Babel
from config import HOST, PORT, USERNAME, PASSWORD, DB_NAME
from models.category import CategoryView, FilmCategory, BookCategory, OutcomingCategory, IncomingCategory, TaskCategory
from models.finances.operations.incoming import IncomingOperation, IncomingOperationView
from models.finances.operations.outcoming import OutomingOperationView, OutcomingOperation
from models.finances.wallet import WalletView, Wallet
from models.library.book import Book, BookView, ReadedBookView
from models.library.film import FilmView, Film, WatchedFilmView
from models.library.place import Place, VisitedPlaceView, PlaceView
from models.tasks.everyday_task import EveryDayTask, EveryDayTaskView
from models.tasks.hanging_task import HangingTask, HangingTaskView
from models.tasks.task import TaskView, Task, ArchiveTasksView, TodayTasksView, ActiveTasksView

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tNc4a7FsdHSvM78kMU'
app.config['MONGODB_SETTINGS'] = {'db': DB_NAME,
                                  'host': HOST,
                                  'port': PORT,
                                  'username': USERNAME,
                                  'password': PASSWORD}

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
    a.add_view(TodayTasksView(Task, name="На сегодня", endpoint="today_tasks", category=cat))
    a.add_view(ActiveTasksView(Task, name="Активные", endpoint="active_tasks", category=cat))
    a.add_view(ArchiveTasksView(Task, name="Архив", endpoint="archive_tasks", category=cat))
    add_divider(a, cat)
    a.add_view(EveryDayTaskView(EveryDayTask, name="Ежедневные", endpoint="everyday_tasks", category=cat))
    add_divider(a, cat)
    a.add_view(HangingTaskView(HangingTask, name="Подвешенные", endpoint="hanging_tasks", category=cat))
    a.add_view(TaskView(Task, name="Все дела", endpoint="tasks"))


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


if __name__ == '__main__':
    admin = admin.Admin(app, 'LIFE', base_template='layout.html', template_mode='bootstrap3')
    add_tasks_menu(admin)
    add_finances_menu(admin)
    add_lib_menu(admin)
    add_settings_menu(admin)

    app.run(host="192.168.0.102", debug=True, use_reloader=True)
