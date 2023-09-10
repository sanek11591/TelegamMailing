import multiprocessing
import time
from multiprocessing import Process
from telebot import TeleBot
import psycopg2

bot = TeleBot('6562747970:AAGcckmVkQqbqkBmkAQT4Jw70xe23t9EEg4')


def lister_of_base():
    print('Start monitoring base')
    task_queue = multiprocessing.Queue()
    process_collect_records = Process(target=collect_records_from_database, args=(task_queue,))
    process_mailing_to_users = Process(target=send_mailing_to_users, args=(task_queue,))
    process_collect_records.start()
    process_mailing_to_users.start()


def connect_to_base(request):
    conn = psycopg2.connect(dbname='habrdb', user='habrpguser',
                            password='pgpwd4habr', host='localhost')
    cursor = conn.cursor()
    cursor.execute(request)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records


def collect_records_from_database(task_queue):
    while True:
        time.sleep(1)
        records = connect_to_base(
            f"SELECT massege,send_time,id FROM mailing WHERE send_time = timezone('utc-3', now())::timestamp(0)")
        if records:
            for record in records:
                task_queue.put(record)


def send_mailing_to_users(task_queue):
    while True:
        mail = task_queue.get()
        print('mailing found to be processed: {}'.format(mail))
        user_ids = connect_to_base(f"SELECT user_id FROM users")
        for user_id in user_ids:
            print(user_id[0])
            bot.send_message(user_id[0], f"{mail[0]}")
