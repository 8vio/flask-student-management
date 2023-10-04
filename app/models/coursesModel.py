from app.db import BaseModelMixin, db, TimeStampedMixin
from sqlalchemy.sql import func

class Courses(TimeStampedMixin, BaseModelMixin):
    __tablename__ = 'courses'

    id_course= db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.Text, nullable=False)
    dt_created = db.Column(db.DateTime, nullable=False, server_default=func.now())
    ic_active = db.Column(db.Boolean, default=True)


    def __init__(
            self,
            course_name,
            dt_created = func.now(),
            ic_active=True
    ):
        super().__init__()
        self.course_name = course_name
        self.dt_created = dt_created
        self.ic_active = ic_active

    def __repr__(self):
        return f'MyModel({self.id_course})'

    def __str__(self):
        return f'{self.id_course}'
    
    def to_dict(self):
        return {
            "id_course": self.id_course,
            "course_name": self.course_name,
            "dt_created": self.dt_created.strftime("%m/%d/%Y"),
            "ic_active": self.ic_active
        }




