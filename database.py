import sqlite3

conn = sqlite3.connect('todo.db')
# print ("Opened database successfully")

conn.execute('''CREATE TABLE todo (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Task  TEXT    NOT NULL,
    Status            TEXT     NOT NULL);''')
# print ("Table created successfully")

conn.close()