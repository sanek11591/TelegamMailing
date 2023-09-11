import multiprocessing
import time
from multiprocessing import Process
from telebot import TeleBot
import psycopg2
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = TeleBot('6562747970:AAGcckmVkQqbqkBmkAQT4Jw70xe23t9EEg4')


def lister_of_base():
    print('Start monitoring base')
    task_queue = multiprocessing.Queue()
    process_collect_records = Process(target=collect_records_from_database, args=(task_queue,))
    process_mailing_to_users = Process(target=send_mailing_to_users, args=(task_queue,))
    process_monitor_overdue = Process(target=monitor_overdue)
    process_collect_records.start()
    process_mailing_to_users.start()
    process_monitor_overdue.start()


def connect_to_base(request, record=False):
    conn = psycopg2.connect(dbname='habrdb', user='habrpguser',
                            password='pgpwd4habr', host='localhost')
    cursor = conn.cursor()
    cursor.execute(request)
    if record:
        conn.commit()
    else:
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
            bot.send_message(user_id[0], f"{mail[0]}", reply_markup=gen_markup(mail[2]))
        connect_to_base(f"update mailing set status = 'done' where id = {mail[2]}", True)


def gen_markup(mail_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Да", callback_data="cb_yes:"+str(mail_id)),
               InlineKeyboardButton("Нет", callback_data="cb_no:"+str(mail_id)))
    return markup


def monitor_overdue():
    while True:
        time.sleep(20)
        overdue_transactions = connect_to_base(
            f"select * from mailing where send_time < timezone('utc-3', now())::timestamp(0)")
        if overdue_transactions:
            for transaction in overdue_transactions:
                connect_to_base(
                    f"update mailing set status = 'overdue' where id = {transaction[0]} and status = 'create'",
                    True)
