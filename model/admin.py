import psycopg2
from telebot import types

stage = {}
text = {}


class Admin:

    @staticmethod
    async def admin_keyboard(bot, chat_id):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Добавить рассылку')
        itembtn2 = types.KeyboardButton('Удалить рассылку')
        markup.add(itembtn1, itembtn2)
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
