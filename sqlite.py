import sqlite3


def sql_connect():
    try:
        connection = sqlite3.connect("sqlite3.db")  # SQLite3 bazasiga bog'lanish
        connection.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False


def sql_connection():
    connection = sqlite3.connect("sqlite3.db")  # SQLite3 bazasiga bog'lanish
    connection.commit()
    return connection


def CreateTableAPI():
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        create_table = """ CREATE TABLE api_key (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid BIGINT NOT NULL,
                api_key TEXT NOT NULL,
                url TEXT NOT NULL
            ); """
        cursor.execute(create_table)
        conn.commit()
    else:
        return False


def AddPayCard(name, card, info):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO pay_card (name, card, info) VALUES (?, ?, ?)""",
                (name, card, info),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False


def select_info(id):
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {id}")

        res = cursor.fetchall()
        conn.commit()
        l = list()
        if not res:
            return False
        else:
            for i in res:
                l.append(i)
            return l
    else:
        return False


def dalete_info(id):

    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {id}")

            conn.commit()
            conn.close
            return True
        except:
            return False
    else:
        return False


def delete_table(da, ta, keys):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {da} WHERE {ta} = {keys}")
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def drop_table(keys):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()
            cursor.execute(f"drop table {keys}")
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
    else:
        return False


def UpdateRaferalCount(id, count):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET offer = ? WHERE uid = ?", (count, id))
            con.commit()
            print(f"Updated ID: {id} with offer: {count}")  # Logging
            return True
    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")  # Logging
        return False


def table_info(ab, ba, id):
    if sql_connect() == True:

        conn = sql_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {ab} WHERE {ba} = ?", (id,))

        res = cursor.fetchall()
        conn.commit()

        if not res:
            return False
        else:
            return res
    else:
        return False


def one_table_info(ab, ba, id):
    if sql_connect() == True:

        conn = sql_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {ab} WHERE {ba} = ?", (id,))

        res = cursor.fetchone()
        conn.commit()

        if not res:
            return False
        else:
            return res
    else:
        return False