import psycopg2


def is_admin_check(message):
    conn = psycopg2.connect(dbname='habrdb', user='habrpguser',
                            password='pgpwd4habr', host='localhost')
    cursor = conn.cursor()
    cursor.execute(f'SELECT user_id, role FROM users WHERE user_id={message.from_user.id}')
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    if records[0][1] == 'admin':
        return True
    else:
        return False


def add_new_user(user_id, role, user_name):
    conn = psycopg2.connect(dbname='habrdb', user='habrpguser',
                            password='pgpwd4habr', host='localhost')
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO users (user_id, role, user_name) VALUES ({user_id}, '{role}', '{user_name}')")
    conn.commit()
    conn.close()
