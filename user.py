import dbhandler

class User():
    def __init__(self, email):
        self.email = email
        self.fetch_db()

    def fetch_db(self):
        UserDB = dbhandler.UserDB()
        self.name, self.nickname = UserDB.get_name_nickname(self.email)
        print(self.name, self.nickname)
