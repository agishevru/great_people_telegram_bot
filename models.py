""" Модуль, создающий подключение к БД и все основные модели с помощью Pony.orm """

from pony.orm import Database, Required, Optional, Set, PrimaryKey, db_session
from config import DB_CONFIG

db = Database()


class User(db.Entity):
    """ Карточка пользователя """
    user_id = Optional(int, size=64)
    username = Optional(str)
    name = Optional(str)
    surname = Optional(str)
    time = Optional(str)
    selected_character = Optional(str)



class Dialogs(db.Entity):
    """ Таблица, содержащая запросы пользователей и ответы ИИ """
    response_id = PrimaryKey(int, auto=True)
    user = Optional(int, size=64)
    character_name = Optional(str)
    user_message = Optional(str)
    character_message = Optional(str)
    time = Optional(str)


class Amplitude(db.Entity):
    """ Имитация сервиса аналитики Amplitude """
    user_id = Optional(int, size=64)
    act = Optional(str)
    time = Optional(str)


class Welcome_text(db.Entity):
    """ Приветственные сообщения персонажей """
    character_name = Optional(str)
    text = Optional(str)


db.bind(**DB_CONFIG)
db.generate_mapping(create_tables=True)


# ------ заполнение Welcome_text -------
@db_session
def write_in_welcome_text() -> None:
    """ Заполнение приветствий """
    text_einshteyn = 'Приветствую вас, уважаемый собеседник! Я - Альберт Эйнштейн, известный как тот парень, который любил физику,' \
                     ' фантастическую укладку и загадки Вселенной. Можно сказать, я наделал черных дыр в науке, а мои мысли летали' \
                     ' быстрее света (по крайней мере, в моей голове). Но сегодня я здесь, чтобы помочь вам с вашими вопросами и' \
                     ' размышлениями. Как я могу быть полезен?'
    text_mario = 'Привет! Я - Марио, известный как тот чувак в красной шапке.. Моя профессия? ' \
                 'Спасать принцессу, конечно. И делать это в любой не понятной ситуации. Сегодня я здесь, чтобы добавить немного ' \
                 'приключений и радуги в ваш день. Чем могу помочь, приятель?'

    Welcome_text(character_name='Альберт Эйнштейн', text=text_einshteyn)
    Welcome_text(character_name='Марио', text=text_mario)
    db.commit()

# заполнение
@db_session
def check_and_initialize_welcome_text():
    if not Welcome_text.select(): write_in_welcome_text()

check_and_initialize_welcome_text()
# ------------------------------------------------
