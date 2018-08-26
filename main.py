from flask import Flask

import flask_admin as admin
from flask_admin.menu import MenuLink
from flask_mongoengine import MongoEngine

# Create application
from config import HOST, PORT, USERNAME, PASSWORD, DB_NAME
from models.finances.incoming import IncomingOperation, IncomingOperationView
from models.finances.incoming_category import IncomingCategoryView, IncomingCategory
from models.finances.outcoming import OutomingOperationView, OutcomingOperation
from models.finances.outcoming_category import OutcomingCategoryView, OutcomingCategory
from models.finances.wallet import WalletView, Wallet
from models.library.book import Book, BookView, ReadedBookView
from models.library.book_category import BookCategory, BookCategoryView
from models.library.film import FilmView, Film, WatchedFilmView
from models.library.film_category import FilmCategoryView, FilmCategory
from models.tasks.everyday_task import EveryDayTask, EveryDayTaskView
from models.tasks.hanging_task import HangingTask, HangingTaskView
from models.tasks.task import TaskView, Task, ArchiveTasksView, TodayTasksView, ActiveTasksView
from models.tasks.task_category import TaskCategoryView, TaskCategory

app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = 'tNc4a7FsdHSvM78kMU'
app.config['MONGODB_SETTINGS'] = {'db': DB_NAME,
                                  'host': HOST,
                                  'port': PORT,
                                  'username': USERNAME,
                                  'password': PASSWORD}

# Create models
db = MongoEngine()
db.init_app(app)

if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, 'LIFE', base_template='layout.html', template_mode='bootstrap3')

    # Add views
    admin.add_view(TodayTasksView(Task, name="На сегодня", endpoint="today_tasks", category="Дела"))
    admin.add_view(ActiveTasksView(Task, name="Активные", endpoint="active_tasks", category="Дела"))
    admin.add_view(ArchiveTasksView(Task, name="Архив", endpoint="archive_tasks", category="Дела"))
    admin.add_menu_item(MenuLink("", url="#", class_name="divider"), target_category="Дела")
    admin.add_view(EveryDayTaskView(EveryDayTask, name="Ежедневные", endpoint="everyday_tasks", category="Дела"))
    admin.add_menu_item(MenuLink("", url="#", class_name="divider"), target_category="Дела")
    admin.add_view(HangingTaskView(HangingTask, name="Подвешенные", endpoint="hanging_tasks", category="Дела"))
    admin.add_view(TaskView(Task, name="Все дела", endpoint="tasks"))

    admin.add_view(IncomingOperationView(IncomingOperation, name="Доходы", endpoint="incoming", category="Финансы"))
    admin.add_view(OutomingOperationView(OutcomingOperation, name="Расходы", endpoint="outcoming", category="Финансы"))
    admin.add_menu_item(MenuLink("", url="#", class_name="divider"), target_category="Финансы")
    admin.add_view(WalletView(Wallet, name="Кошельки", endpoint="wallets", category="Финансы"))

    admin.add_view(TaskCategoryView(TaskCategory, name="Категории дел", endpoint="tasks_categories", category="Настройки"))
    admin.add_menu_item(MenuLink("", url="#", class_name="divider"), target_category="Настройки")
    admin.add_view(IncomingCategoryView(IncomingCategory, name="Категории доходов", endpoint="incoming_categories", category="Настройки"))
    admin.add_view(OutcomingCategoryView(OutcomingCategory, name="Категории расходов", endpoint="outcoming_categories", category="Настройки"))
    admin.add_menu_item(MenuLink("", url="#", class_name="divider"), target_category="Настройки")
    admin.add_view(BookCategoryView(BookCategory, name="Жанры книг", endpoint="book_categories",
                                         category="Настройки"))
    admin.add_view(FilmCategoryView(FilmCategory, name="Жанры фильмов", endpoint="film_categories",
                                    category="Настройки"))

    admin.add_view(BookView(Book, name="Книги", endpoint="books",
                                         category="Библиотека"))
    admin.add_view(ReadedBookView(Book, name="Прочитанные книги", endpoint="readed_books",
                            category="Библиотека"))
    admin.add_menu_item(MenuLink("", url="#", class_name="divider"), target_category="Библиотека")
    admin.add_view(FilmView(Film, name="Фильмы", endpoint="films",
                            category="Библиотека"))
    admin.add_view(WatchedFilmView(Film, name="Просмотренные фильмы", endpoint="watched_films",
                                  category="Библиотека"))
    # admin.add_menu_item(MenuLink("test", url="#", class_name="divider"), target_category="Логи")
    # Start app
    app.run(host="127.0.0.1",debug=True,use_reloader=True)
