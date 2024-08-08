import sqlite3
from sqlite3 import Error


def create_table():
    try:
        connection= sqlite3.connect('sqlite3.db')

        table = """ CREATE TABLE Users (
                    user_id BIGINT NOT NULL ,
                    fullname TEXT NOT NULL ,
                    username TEXT NOT NULL ,
                    phone TEXT NOT NULL 
                ); """
        cursor = connection.cursor()
        print("databaza yaratildi")
        cursor.execute(table)
        cursor.close()
    
    except Error as error:
        print("hatolik", error)
    finally:
        if connection:
            connection.close()    
            print("sqlite o'chdi")
# create_table()
            

def Add_db(user_id, fullname, username, phone):
    try:
        with sqlite3.connect("sqlite3.db") as connection:
            cursor = connection.cursor()
            
            table = '''
                INSERT INTO Users(user_id, fullname, username, phone) VALUES(?, ?, ?, ?)
            '''
            cursor.execute(table, (user_id, fullname, username, phone))
            connection.commit()
            print("SQLite tablega qo'shildi")
            cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if connection:
            connection.close()
            # print("Sqlite ish foalyatini tugatdi")      


def Read_db():
    try:
        with sqlite3.connect("sqlite3.db") as sqliteconnection:
            cursor = sqliteconnection.cursor()
            sql_query = """
                SELECT * FROM Users 
            """
        
            cursor.execute(sql_query) 
            A = cursor.fetchall()
            print("table oqildi")
            return A

    except Error as error:
        print("xatolik:", error)
    finally:
        if sqliteconnection:
            sqliteconnection.close()
            # print("sqlite faoliyatini tugatdi")                        