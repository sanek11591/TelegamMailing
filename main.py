from controller import controller
import asyncio
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot('token')

if __name__ == '__main__':
    controller.Controller(bot)
    asyncio.run(bot.polling(non_stop=True))
