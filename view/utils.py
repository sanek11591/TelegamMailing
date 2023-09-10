import multiprocessing
import time
from multiprocessing import Process
from telebot import TeleBot
import psycopg2

bot = TeleBot('6562747970:AAGcckmVkQqbqkBmkAQT4Jw70xe23t9EEg4')


def lister_of_base():
    print('Start monitoring base')
    task_queue = multiprocessing.Queue()
    process_one = Process(target=sendler, args=(task_queue,))
    process_two = Process(target=my_consumer, args=(task_queue,))
    process_one.start()
    process_two.start()


def sendler(q):
    while True:
        time.sleep(1)
        conn = psycopg2.connect(dbname='habrdb', user='habrpguser',
                                password='pgpwd4habr', host='localhost')
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT massege,send_time,id FROM mailing WHERE send_time = timezone('utc-3', now())::timestamp(0)")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        if records:
            for i in records:
                q.put(i)


def my_consumer(q):
    while True:
        data = q.get()
        print('data found to be processed: {}'.format(data))
        conn = psycopg2.connect(dbname='habrdb', user='habrpguser',
                                password='pgpwd4habr', host='localhost')
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT user_id FROM users")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        for i in records:
            print(i)
            bot.send_message(i[0], f"{data[0]}")
