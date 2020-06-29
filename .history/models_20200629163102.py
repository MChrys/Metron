import enum
class Character(db.Model):
    Id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String())
    Age = db.Coulmn(db.Integer())
    Weight = db.Column()

class ColorType(enum.Enum):
    PURPLE = "PURPLE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

class Hat(db.Model):
    Id = db.Column(db.Integer(), primary_key = True)
    Color = db.Column(db.Enum(ColorType))