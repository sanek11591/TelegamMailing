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

        @self.bot.message_handler(content_types=['text'])
        async def send_command_to_admin(message):
            if utils.is_admin_check(message):
                if message.text == 'Добавить рассылку' or message.chat.id in self.flag:
                    if message.chat.id not in self.flag:
                        self.flag.append(await Admin.add_mailing(bot, message.chat.id, message.text))
                    else:
                        if await Admin.add_mailing(bot, message.chat.id, message.text) == 0:
                            self.flag.remove(message.chat.id)
                elif message.text == 'Удалить рассылку':
                    await self.bot.send_message(message.chat.id, 'Удаление будет позже')
                elif message.text == '/admin':
                    await Admin.admin_keyboard(self.bot, message.chat.id)
                else:
                    await self.bot.send_message(message.chat.id, "Команда не существует")
            else:
                await self.bot.send_message(message.chat.id, "Команда не существует или не доступна")
