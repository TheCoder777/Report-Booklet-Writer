import dbhandler

class User():
    def __init__(self, id=0, email="", name="", nickname=""):
        self.email = email
        self.name = name
        self.nickname = nickname
        self.id = id
        if not len(nickname):
            self.nickname = self.name
        self.fetch_db()


    def fetch_db(self):
        UserDB = dbhandler.UserDB()
        if self.id:
            self.name, self.nickname, self.email = UserDB.fetch_by_id(self.id)
        # if len(self.email) and len(self.name) and len(self.nickname):
        #     return True
        # elif len(self.nickname):
        #     self.name, self.email = UserDB.get_name_email_by_nickname(self.nickname)
        # elif len(self.email):
        #     self.name, self.nickname = UserDB.get_name_nickname_by_email(self.email)
        else:
            pass
