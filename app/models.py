from . import db
from . import login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

 


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'


class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    cotegory = db.Column(db.String(255))
    upvote= db.Column(db.Integer)
    downvote = db.Column(db.Integer)
    
    # users = db.relationship('User',backref = 'role',lazy="dynamic")
    # all_pitchs = []
     # Some code is here
    # @classmethod
    # def get_pitchs(cls,id):
    #     response = []

    #     for pitch in cls.all_pitchs:
    #         if pitch.pitche_id == id:
    #             response.append(pitch)

    #     return response
    def __repr__(self):
        return f'User {self.description}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))

    def __repr__(self):
        return f'User {self.comment}'
    

