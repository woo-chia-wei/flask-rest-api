import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# Use INTEGER instead of INT to set autoincrement
create_table = "CREATE TABLE IF NOT EXISTS users \
               (id INTEGER PRIMARY KEY,  \
                username text, \
                password text)" 

cursor.execute(create_table)

connection.commit()

connection.close()