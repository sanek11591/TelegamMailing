from controller import controller
import asyncio
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot('6562747970:AAGcckmVkQqbqkBmkAQT4Jw70xe23t9EEg4')

if __name__ == '__main__':
    controller.Controller(bot)
    asyncio.run(bot.polling(non_stop=True))
