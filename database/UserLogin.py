import database.request_DB


class UserLogin():
    def fromDB(self, user_id, db):
        self.__user = database.request_DB.get_user_id()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True;

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])
