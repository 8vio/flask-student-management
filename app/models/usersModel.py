from app.db import BaseModelMixin, db, TimeStampedMixin
from sqlalchemy.sql import func

class Users(TimeStampedMixin, BaseModelMixin):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    st_firstname = db.Column(db.Text, nullable=False)
    st_lastname = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    em_user_email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    dt_created = db.Column(db.DateTime, nullable=False, server_default=func.now())
    ic_active = db.Column(db.Boolean, default=True)

    def __init__(
            self,
            st_firstname,
            st_lastname,
            username,
            em_user_email,
            password,
            dt_created = func.now(),
            ic_active=True
    ):
        super().__init__()
        self.st_firstname = st_firstname
        self.st_lastname = st_lastname
        self.username = username
        self.em_user_email = em_user_email
        self.password = password
        self.dt_created = dt_created
        self.ic_active = ic_active

    def __repr__(self):
        return f'MyModel({self.id_user})'

    def __str__(self):
        return f'{self.id_user}'
    
    def to_dict(self):
        return {
            "id_user": self.id_user,
            "st_firstname": self.st_firstname,
            "st_lastname": self.st_lastname,
            "username": self.username,
            "em_user_email": self.em_user_email,
            "dt_created": self.dt_created.strftime("%m/%d/%Y"),
            "ic_active": self.ic_active
        }




