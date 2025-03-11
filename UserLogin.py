import database.request_DB
from flask_login import UserMixin
from flask import url_for

class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = database.request_DB.get_user_id(user_id)
        self.name = self.__user['username']
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return str(self.__user['username'])

    def getEmail(self):
        return str(self.__user['email'])

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='img/ava.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("No file ava" + str(e))
        else:
            img = self.__user['avatar']
        return img

    def verifyExt(self, filename: str):
        ext = filename.rsplit('.',1)[1]
        if ext == "png" or ext == "PNG":
            return True
        return False
