class User:
    def __init__(self, _id, username, password): # _id instead of id because id is keyword
        self.id = _id
        self.username = username
        self.password= password