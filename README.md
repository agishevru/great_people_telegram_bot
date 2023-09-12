Great people telegram bot
=========================

Тестовый бот. Реализован на `Python 3.10`. И в качестве базы даных использует `SQLite`.
---

Для запуска:
-----------
1. Необходимо создать `config.py` и прописать свои ключи API от telegram и ChatGPT:

```python
TOKEN = 'свой ключ API telegram'
OPENAI_API_KEY = 'свой ключ API ChatGPT'
```

2. Нужно разместить html страницу с выбором персонажей - `character.html` на хостинге, или в GitHub Pages.
Указать ее адрес в функции клавиатуры модуля `app.py`:
```python
def keyboard() -> ReplyKeyboardMarkup:
    """ Клавиатура выбора персонажа """
    keyboard = ReplyKeyboardMarkup.from_button(
        resize_keyboard=True,
        button=KeyboardButton(
                text="Выбрать персонажа",
                web_app=WebAppInfo(url="ВАШ_АДРЕС/character.html")))
    return keyboard
```

3. Далее установить виртуальное окружение и зависимости из `requirements.txt`.
В активированном виртуальном окружении запустите:

```shell
python app.py
```

Если все успешно, бот начнет выводить в консоль логи о событиях.