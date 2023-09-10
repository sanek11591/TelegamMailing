import psycopg2
from telebot import types

import model.utils
import view.utils

stage = {}
text = {}


class Admin:

    @staticmethod
    async def admin_keyboard(bot, chat_id):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        add_mailing = types.KeyboardButton('Добавить рассылку')
        delete_mailing = types.KeyboardButton('Удалить рассылку')
        markup.add(add_mailing, delete_mailing)
        await bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

    @staticmethod
    async def add_mailing(bot, chat_id, message):
        if chat_id not in stage:
            await bot.send_message(chat_id, "Введите текст рассылки:")
            stage[chat_id] = 1
            return chat_id
        elif stage[chat_id] == 1:
            text[chat_id] = message
            await bot.send_message(chat_id, "Введите дату рассылки в формате YYYY-MM-DD hh:mm:ss")
            stage[chat_id] = 2
            return chat_id
        elif stage[chat_id] == 2:
            if model.utils.date_check(message):
                conn = psycopg2.connect(dbname='habrdb', user='habrpguser',
                                        password='pgpwd4habr', host='localhost')
                cursor = conn.cursor()
                cursor.execute(
                    f"INSERT INTO mailing (massege, send_time, status) VALUES ('{text[chat_id]}', '{message}', 'create')")
                conn.commit()
                conn.close()
                await bot.send_message(chat_id, f"Добавлена рассылка на {message}")
                del stage[chat_id]
                del text[chat_id]
                return 0
            else:
                await bot.send_message(chat_id, f"Неверный формат даты")

    @staticmethod
    async def del_mailing(bot, chat_id):
        for i in view.utils.connect_to_base('select * from mailing'):
            await bot.send_message(chat_id, f'id:{i[0]} \nmessage: {i[1]} \ndate: {i[2]} \nstatus: {i[3]}')
