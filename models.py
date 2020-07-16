import enum
from init_app import db 


from enum import Enum, auto
class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class ColorHat(AutoName):
    PURPLE = auto()
    YELLOW = auto()
    GREEN = auto()

class Hat(db.Model):
    __tablename__ = 'hat'
    Id = db.Column(db.Integer(), primary_key = True)
    Color = db.Column(db.Enum(ColorHat))
    #character = db.relationship("Character", uselist=False, back_populates="hat")
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,Color):
        self.Color = ColorHat[Color]

    def __repr__(self):
        return '' % self.Id


class Character(db.Model):
    __tablename__ = 'character'
    Id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String(), nullable=False)
    Age = db.Column(db.Integer(), nullable=False)
    Weight = db.Column(db.Integer() ,nullable=False)
    Human = db.Column(db.Boolean(), nullable=False)
    Hat_id = db.Column(db.Integer(), db.ForeignKey('hat.Id'), nullable =True)
    #Hat = db.relationship("Hat", back_populates ="character", single_parent= True,uselist=False, cascade = "all, delete, delete-orphan" )
    Hat = db.relationship("Hat", single_parent= True,uselist=False, cascade = "all, delete, delete-orphan" )

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,Name,Age,Weight,Human,Hat):
        self.Name = Name
        self.Age = Age
        self.Weight = Weight
        self.Human = Human
        self.Hat = Hat
    def __repr__(self):
        return '' % self.Id

db.create_all()