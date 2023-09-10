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
        cancel = types.KeyboardButton('Отмена')
        markup.add(add_mailing, delete_mailing, cancel)
        await bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

    @staticmethod
    async def add_mailing(bot, chat_id, message):

        if message == 'Отмена':
            if chat_id in stage.keys():
                del stage[chat_id]
            if chat_id in text.keys():
                del text[chat_id]
            return 0
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
                view.utils.connect_to_base(
                    f"INSERT INTO mailing (massege, send_time, status) VALUES ('{text[chat_id]}', '{message}', 'create')",
                    True)
                await bot.send_message(chat_id, f"Добавлена рассылка на {message}")
                del stage[chat_id]
                del text[chat_id]
                return 0
            else:
                await bot.send_message(chat_id, f"Неверный формат даты")

    @staticmethod
    async def del_mailing(bot, chat_id, message):
        if message == 'Удалить рассылку':
            for i in view.utils.connect_to_base('select * from mailing'):
                await bot.send_message(chat_id, f'id:{i[0]} \nmessage: {i[1]} \ndate: {i[2]} \nstatus: {i[3]}')
            await bot.send_message(chat_id, f'Укажите номера id через запятую')
            return chat_id
        elif message == 'Отмена':
            return 0
        else:
            message = message.split(',')
            for i in message:
                view.utils.connect_to_base(f'delete from mailing where id = {i}', True)
            return 0
