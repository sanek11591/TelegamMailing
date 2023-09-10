from threading import Thread

import view.utils
from model import utils
from model.admin import Admin


class Controller:
    def __init__(self, bot):
        self.bot = bot
        self.flag = []
        t = Thread(target=view.utils.lister_of_base)
        t.start()

        @self.bot.message_handler(commands=['admin'])
        async def send_message_to_model(message):
            if utils.is_admin_check(message):
                await Admin.admin_keyboard(self.bot, message.chat.id)
            else:
                await self.bot.send_message(message.chat.id, "Команда не доступна")

        @self.bot.message_handler(content_types=['text'])
        async def send_command_to_admin(message):
            if message.text == 'Добавить рассылку' or message.chat.id in self.flag:
                if utils.is_admin_check(message):
                    if message.chat.id not in self.flag:
                        self.flag.append(await Admin.add_mailing(bot, message.chat.id, message.text))
                    else:
                        if await Admin.add_mailing(bot, message.chat.id, message.text) == 0:
                            self.flag.remove(message.chat.id)
                else:
                    await self.bot.send_message(message.chat.id, "Команда не доступна")
            if message.text == 'Удалить рассылку':
                if utils.is_admin_check(message):
                    await self.bot.send_message(message.chat.id, 'Удаление будет позже')
                else:
                    await self.bot.send_message(message.chat.id, "Команда не доступна")
            else:
                await self.bot.send_message(message.chat.id, "Команда не существует")
