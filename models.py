import enum
class Character(db.Model):
    Id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String())
    Age = db.Coulmn(db.Integer())
    Weight = db.Column()
    Hat = relationship(Hat, uselist=False, nullable=True)

from enum import Enum, auto
class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class ColorHat(AutoName):
    PURPLE = auto()
    YELLOW = auto()
    GREEN = auto()

class Hat(db.Model):
    Id = db.Column(db.Integer(), primary_key = True)
    Color = db.Column(db.Enum(ColorHat))