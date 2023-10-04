from app.db import BaseModelMixin, db, TimeStampedMixin
from sqlalchemy.sql import func

class Students(TimeStampedMixin, BaseModelMixin):
    __tablename__ = 'students'

    id_student = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    family_name = db.Column(db.Text, nullable=False)
    date_birth = db.Column(db.DateTime, nullable=False)
    email_address = db.Column(db.Text, nullable=False)
    dt_created = db.Column(db.DateTime, nullable=False, server_default=func.now())
    ic_active = db.Column(db.Boolean, default=True)


    def __init__(
            self,
            first_name,
            family_name,
            date_birth,
            email_address,
            dt_created = func.now(),
            ic_active=True
    ):
        super().__init__()
        self.first_name = first_name
        self.family_name = family_name
        self.date_birth = date_birth
        self.email_address = email_address
        self.dt_created = dt_created
        self.ic_active = ic_active

    def __repr__(self): # pragma: no cover
        return f'MyModel({self.id_student})'

    def __str__(self): # pragma: no cover
        return f'{self.id_student}'
    
    def to_dict(self):
        return {
            "id_student": self.id_student,
            "first_name": self.first_name,
            "family_name": self.family_name,
            "date_birth": self.date_birth,
            "email_address": self.email_address,
            "dt_created": self.dt_created.strftime("%m/%d/%Y"),
            "is_active": self.ic_active
        }




