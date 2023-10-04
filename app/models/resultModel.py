from app.db import BaseModelMixin, db, TimeStampedMixin
from sqlalchemy.sql import func

class Results(TimeStampedMixin, BaseModelMixin):
    __tablename__ = 'results'

    id_result= db.Column(db.Integer, primary_key=True)
    cd_student = db.Column(db.Integer, nullable=False)
    cd_course = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Text, nullable=False)
    dt_created = db.Column(db.DateTime, nullable=False, server_default=func.now())
    ic_active = db.Column(db.Boolean, default=True)

    def __init__(
            self,
            cd_student,
            cd_course,
            score,
            dt_created = func.now(),
            ic_active=True
    ):
        super().__init__()
        self.cd_student = cd_student
        self.cd_course = cd_course
        self.score = score
        self.dt_created = dt_created
        self.ic_active = ic_active

    def __repr__(self):  # pragma: no cover
        return f'MyModel({self.id_result})'

    def __str__(self):  # pragma: no cover
        return f'{self.id_result}'
    
    def to_dict(self):
        return {
            "id_result": self.id_result,
            "cd_student": self.cd_student, 
            "cd_course": self.cd_course,
            "score": self.score,
            "dt_created": self.dt_created.strftime("%m/%d/%Y"),
            "ic_active": self.ic_active
        }




