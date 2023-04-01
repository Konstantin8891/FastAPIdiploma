from flask_login import current_user
from sqlalchemy_utils import EmailType, ChoiceType

from admin import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    # return db.query(User).get(user_id)


ROLES = (('admin', 'admin'), ('user', 'user'))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(EmailType)
    username = db.Column(db.String)
    password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    role = db.Column(ChoiceType(ROLES))    

    #-----login requirements-----
    def is_active(self):
    #all users are active
        return True 

    def get_id(self):
        # returns the user e-mail. not sure who calls this
        return str(self.id)

    def is_authenticated(self):
        if current_user.is_authenticated:
            return True
        return False

    def is_anonymous(self):
        # False as we do not support annonymity
        return False

    #constructor
    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
