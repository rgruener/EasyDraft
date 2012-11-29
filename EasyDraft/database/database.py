from flask.ext.mysql import MySQL
from EasyDraft.models import User

class Database():

    def __init__(self, app):
        self.mysql = MySQL()
        self.mysql.init_app(app)

    def get_all_users(self):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT email, password FROM Users"""
        cursor.execute(query)
        rows = cursor.fetchall()
        users = []
        for row in rows:
            users.append(User(row[0], row[1]))
        self.mysql.teardown_request()
        return users


    def get_user(self, email, password=None):
        if email is None:
            return None
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        query = """SELECT email, password FROM Users WHERE email = '%s'""" % (email)
        if password:
            query += """ AND password = '%s'""" % (password)
        cursor.execute(query)
        u = cursor.fetchone()
        cursor.close()
        self.mysql.teardown_request()
        if not u:
            return None
        return User(u[0], u[1])

    def insert_user(self, email, password):
        self.mysql.before_request()
        cursor = self.mysql.get_db().cursor()
        if (not (email and password)):
            return False
        statement = """INSERT INTO Users (email, password) VALUES ('%s', '%s')""" % (email, password)
        cursor.execute(statement)
        self.mysql.get_db().commit()
        cursor.close()
        self.mysql.teardown_request()
        return True
