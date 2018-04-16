import sqlite3

class User:
    def __init__(self, _id, username, password): # _id instead of id because id is keyword
        self.id = _id
        self.username = username
        self.password= password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,)) # way to create tuple with single value
        row = result.fetchone()

        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row) # same as above, shorter syntax
        else:
            user = None

        connection.close()
        return user
    
    @classmethod
    def find_by_userid(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user
