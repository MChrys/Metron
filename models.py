import enum
from app import db 
class Character(db.Model):
    __tablename__ = 'characters'
    Id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String(), nullable=False)
    Age = db.Coulmn(db.Integer(), nullable=False)
    Weight = db.Column(db.Integer() ,nullable=False)
    Human = db.Column(db.Boolean(), nullable=False)
    Hat = relationship(Hat, uselist=False, nullable=True, cascade = "all, delete, delete-orphan" )
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,Name,Age,Weight,Hat):
        self.Name = Name
        self.Age = Age
        self.Weight = Weight
        self.Hat = Hat
    def __repr__(self):
        return '' % self.Id

from enum import Enum, auto
class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class ColorHat(AutoName):
    PURPLE = auto()
    YELLOW = auto()
    GREEN = auto()

class Hat(db.Model):
    __tablename__ = 'hats'
    Id = db.Column(db.Integer(), primary_key = True)
    Color = db.Column(db.Enum(ColorHat))
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,Color):
        self.Color = Color

    def __repr__(self):
        return '' % self.Id


db.create.all()