from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(80), unique=False, nullable=True)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)
    character_id=db.Column(db.Integer, db.ForeignKey("people.id"))
    
    favorites = db.relationship("Favorite", back_populates="users")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    __tablename__="people"
    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), nullable=False)
    age=db.Column(db.Integer, nullable=False)
    eye_color=db.Column(db.String(40),nullable=False)
    skin_color = db.Column(db.String(80),nullable=False)
    

    favorites = db.relationship("Favorite", back_populates="people")
    
    def __repr__(self):
        return '<User %r>' % self.name


    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "age":self.age,
            "eye_color":self.eye_color,
            "skin_color":self.skin_color
        }

class Planet(db.Model):
    __tablename__="planets"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)
    climate=db.Column(db.String(80), nullable=False)
    gravity=db.Column(db.Integer, nullable=False)
    
    favorites = db.relationship("Favorite", back_populates="planets")

    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "climate":self.climate,
            "graviy":self.gravity
        }
    
class Favorite(db.Model):
    __tablename__="favorites"
    id= db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    people_id=db.Column(db.Integer, db.ForeignKey("people.id"))
    planet_id=db.Column(db.Integer, db.ForeignKey("planets.id"))

    users = db.relationship("User", back_populates ="favorites")
    people = db.relationship("People", back_populates ="favorites")
    planets = db.relationship("Planet", back_populates = "favorites")
    
def serialize(self):
    return{
        "id":self.id,
        "user_id":self.user_id,
        "people_id":self.people_id,
        "planet_id":self.planet_id
    }