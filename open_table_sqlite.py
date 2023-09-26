""" Модуль выводит содержимое таблиц локальной БД SQLite в виде красивых таблиц на консоль. Он уже настроен, нужно
только запустить скрипт. """

import sqlite3
from tabulate import tabulate
import textwrap
import sys


sys.stdout.reconfigure(encoding='utf-8')


class Sqlite3_parser:
    """ Парсер sqlite базы. Выводит данные таблиц в цветном интерфейсе на коносль"""

    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    def __init__(self, db_file: str) -> None:
        """ Инициация парсера, на вход принимает адрес дб: 'db.sqlite' """
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.connection.close()

    def print_table(self, table: str, max_col_widths=None) -> None:
        """ Метод принтует красиво оформленные таблицы. Принимает:
         :param: table='table1' строчное название нужной таблицы
         :param: max_col_widths=[10,20,30] - ширина каждого столбца в таблице
         """
        self.cursor.execute(f"PRAGMA table_info('{table}')")
        self.column_names = [i[1] for i in self.cursor.fetchall()]
        self.cursor.execute(f'SELECT * FROM {table}')
        rows = self.cursor.fetchall()

        if max_col_widths is None:
            max_col_widths = [20] * len(self.column_names)  # Установите ширину по умолчанию

        table_data = []
        for row in rows:
            formatted_row = []
            for i, cell in enumerate(row):
                max_width = max_col_widths[i]
                if isinstance(cell, str) and len(cell) > max_width:
                    # Переносим текст, если он превышает максимальную ширину
                    wrapped_text = textwrap.wrap(cell, width=max_width)
                    formatted_row.append('\n'.join(wrapped_text))
                else:
                    formatted_row.append(cell)
            table_data.append(formatted_row)

        self.data = [[Sqlite3_parser.CYAN + str(i) for i in line] for line in table_data]
        self.table = Sqlite3_parser.YELLOW + tabulate(self.data, headers=self.column_names, tablefmt="pretty")
        print(self.table, end='\n' + Sqlite3_parser.RESET)


# Выводим данные
if __name__ == '__main__':
    db = Sqlite3_parser('bot_database.sqlite')
    db.print_table('User', max_col_widths=[20, 20, 20, 20, 20, 20, 20])
    db.print_table('Dialogs', max_col_widths=[3, 10, 10, 15, 100, 10])
    db.close()