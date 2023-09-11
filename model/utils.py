import datetime
import view.utils


def is_admin_check(message):
    records = view.utils.connect_to_base(f'SELECT user_id, role FROM users WHERE user_id={message.from_user.id}')
    if records[0][1] == 'admin':
        return True
    else:
        return False


def add_new_user(user_id, role, user_name):
    view.utils.connect_to_base(
        f"INSERT INTO users (user_id, role, user_name) VALUES ({user_id}, '{role}', '{user_name}')", True)


def date_check(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
