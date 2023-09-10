from threading import Thread
import view.utils
from model import utils
from model.admin import Admin


class Controller:
    def __init__(self, bot):
        self.bot = bot
        self.flag_receive_command_messages_user = {}
        thread_of_monitoring_database = Thread(target=view.utils.lister_of_base)
        thread_of_monitoring_database.start()

        @self.bot.callback_query_handler(func=lambda call: True)
        async def callback_query(call):
            print()
            answer, mail_id = call.data.split(':')
            if answer == "cb_yes":
                view.utils.connect_to_base(
                    f"INSERT INTO user_answers (mail_id, user_id, answer) VALUES ('{mail_id}', '{call.from_user.id}', '{answer}')",
                    True)
                await bot.answer_callback_query(call.id, "Answer is Yes")
            elif answer == "cb_no":
                view.utils.connect_to_base(
                    f"INSERT INTO user_answers (mail_id, user_id, answer) VALUES ('{mail_id}', '{call.from_user.id}', '{answer}')",
                    True)
                await bot.answer_callback_query(call.id, "Answer is No")

        @self.bot.message_handler(content_types=['text'])
        async def send_command_to_admin(message):
            if utils.is_admin_check(message):
                if message.text == 'Добавить рассылку' or (
                        message.chat.id in self.flag_receive_command_messages_user.keys() and
                        self.flag_receive_command_messages_user[message.chat.id] == 1):
                    if message.chat.id not in self.flag_receive_command_messages_user:
                        self.flag_receive_command_messages_user[message.chat.id] = 1
                        await Admin.add_mailing(bot, message.chat.id, message.text)
                    elif await Admin.add_mailing(bot, message.chat.id, message.text) == 0:
                        del self.flag_receive_command_messages_user[message.chat.id]
                elif message.text == 'Удалить рассылку' or (
                        message.chat.id in self.flag_receive_command_messages_user.keys() and
                        self.flag_receive_command_messages_user[message.chat.id] == 2):
                    if message.chat.id not in self.flag_receive_command_messages_user:
                        self.flag_receive_command_messages_user[message.chat.id] = 2
                        await Admin.del_mailing(bot, message.chat.id, message.text)
                    elif await Admin.del_mailing(bot, message.chat.id, message.text) == 0:
                        del self.flag_receive_command_messages_user[message.chat.id]
                elif message.text == '/admin':
                    await Admin.admin_keyboard(self.bot, message.chat.id)
                elif message.text == "Отмена":
                    await self.bot.send_message(message.chat.id, "Нечего отменять")
                else:
                    await self.bot.send_message(message.chat.id, "Команда не существует")
            else:
                await self.bot.send_message(message.chat.id, "Команда не существует или не доступна")
