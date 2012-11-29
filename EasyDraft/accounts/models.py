from flask.ext.login import UserMixin
from models import User

class User(UserMixin):

    def __init__(self, email, password, active=True):
        self.email = email
        self.password = password
        self.active = active

    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.email)
