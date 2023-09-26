""" Great people telegram bot- бот, имитирующий общение с известными личностями.
 Для запуска необходимо создать config.py и прописать:
 в переменную TOKEN = 'свой ключ API telegram'
 в переменную OPENAI_API_KEY = 'свой ключ API GPT'
 Далее просто запустить файл app.py
 """

from datetime import datetime
import logging
from pprint import pprint

import openai
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from pony.orm import db_session

from config import OPENAI_API_KEY, TOKEN
from models import User, Dialogs, Amplitude, Welcome_text, db
import models


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)
file_handler = logging.FileHandler('tg_bot.log', encoding='utf-8')
log.addHandler(file_handler)  # Привязка к созданному логеру 'Log'




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Подключение пользователя к боту, с созданием профайла в БД User """
    log.info(f'Пользователь {update.effective_user.id} - {update.effective_user.name} - start')
    user = update.message.from_user
    user_id = user.id
    username = user.username
    name = user.first_name
    surname = user.last_name
    time = update.message.date.strftime('%d.%m.%y %H:%M:%S')
    # Сохранение пользователя в БД
    try:
        if not User.get(user_id=user_id):
            new_user = User(user_id=user_id, username=username, name=name, surname=surname, time=time)
            db.commit()
            log.info(f'new_user registred in bd: {new_user.to_dict()}')
            # Amplitude
        send_amplitude_event(user_id, 'registration', time)
    except Exception as exc:
        log.exception(exc)
    # Приветствие
    await update.message.reply_text(
        text="Привет! Здесь можно пообщаться с разными образами известных личностей. Чтобы попробовать - выбери"
             " персонажа, нажав на кнопку. И начни общение на интересующие темы",
        reply_markup=keyboard())
    log.info(f'Пользователь {update.effective_user.id} перешел к выбору персонажа')




async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Получает выбранного пользователем персонажа и записывает его в профайл пользователя """
    log.info(f'Пользователь {update.effective_user.id} - выбрал персонажа {update.effective_message.web_app_data.data}')
    user = User.get(user_id=update.effective_user.id)
    user.selected_character = update.effective_message.web_app_data.data
    welcome_text = Welcome_text.get(character_name=user.selected_character).text
    db.commit()
    # Amplitude
    send_amplitude_event(update.effective_user.id, 'character_selected', update.effective_message.date.strftime('%d.%m.%y %H:%M:%S'))
    await update.message.reply_html(text=welcome_text, reply_markup=keyboard())




async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Отвечает пользователю от лица персонажа """
    log.info(f'Пользователь {update.effective_user.id} спросил - {update.message.text}')
    user = User.get(user_id=update.effective_user.id)
    user_id = update.effective_user.id
    user_message = update.message.text
    time = update.message.date.strftime('%d.%m.%y %H:%M:%S')
    if not user:
        user = User(user_id=user_id, username=update.effective_user.username, name=update.effective_user.username,
                        surname=update.effective_user.last_name,selected_character='Человек', time=time)
        db.commit()
        log.info(f'new_user registred in bd: {user.to_dict()}')


    selected_character = user.selected_character


    # Сохранить сообщение пользователя в дб
    user_question = Dialogs(user=user_id, character_name=selected_character, user_message=user_message, time=time)
    if user_question:
        db.commit()
        log.info(f'user_question - {user_message} сохранен в бд')
    # Amplitude
    send_amplitude_event(user_id, 'user_message_sent', time)
    # API GPT-3
    character_response = call_gpt_api(user_message, selected_character)
    # Сохранить ответ в дб
    user_question.character_message=character_response
    db.commit()
    # Отправить ответ пользователю
    await update.message.reply_html(text=character_response, reply_markup=keyboard())
    # Amplitude
    send_amplitude_event(user_id=user_id, event_name='response_sent', time=datetime.now().strftime('%d.%m.%y %H:%M:%S'))
    log.info(f'Пользователю {update.effective_user.id} ответили - {character_response}')



def call_gpt_api(user_message: str, character_name: str) -> str:
    """ Делает запрос к API GPT от лица выбранного персонажа и возвращает ответ"""
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            # {"role": "system", "content": f"You are {character_name}.Strictly stick to the image and forget you're an artificial intelligence."},
            {"role": "user", "content": user_message}])
    return response.choices[0].message.content



def send_amplitude_event(user_id: int, event_name:str, time:str) -> None:
    """ Здесь имитация взаимодействия с сервисом в Amplitude. Данные о событиях заносятся в модель Amplitude"""
    act = Amplitude(user_id=user_id, act=event_name, time=time)
    db.commit()


def keyboard() -> ReplyKeyboardMarkup:
    """ Клавиатура выбора персонажа """
    keyboard = ReplyKeyboardMarkup.from_button(
        resize_keyboard=True,
        button=KeyboardButton(
                text="Выбрать персонажа",
                web_app=WebAppInfo(url="https://agishevru.github.io/test_work/character.html")))
    return keyboard


@db_session
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    application.add_handler(MessageHandler(filters.TEXT, handle_text))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
