from operator import truediv
from os import name
from flask.helpers import make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

from sqlalchemy.orm import backref, defaultload, relationship
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique=True)
    password = db.Column(db.String(100), nullable = False)
    profile = db.relationship("Profile", cascade="all, delete", backref="users", uselist=False)

    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "password":self.password,
            "bio":self.profile.serialize()
        }

class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String, nullable = False)
    height = db.Column(db.String, nullable = False)
    mass = db.Column(db.String, nullable = False)
    hair_color = db.Column(db.String, nullable = False)
    skin_color = db.Column(db.String, nullable = False)
    eye_color = db.Column(db.String, nullable = False)
    birth_year = db.Column(db.String, nullable = False)
    gender = db.Column(db.String, nullable = False)
    homeworld = db.Column(db.String, nullable = False)

    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "height":self.height,
            "mass":self.mass,
            "hair_color":self.hair_color,
            "skin_color":self.skin_color,
            "eye_color":self.eye_color,
            "birtth_year":self.birth_year,
            "gender":self.gender,
            "homeworld":self.homeworld
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    diameter = db.Column(db.String, nullable = False)
    climate = db.Column(db.String, nullable = False)
    gravity = db.Column(db.String, nullable = False)
    terrain = db.Column(db.String, nullable = False)
    population = db.Column(db.String, nullable = False)

    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "diameter":self.diameter,
            "climate":self.climate,
            "gravity":self.gravity,
            "terrain":self.terrain,
            "population":self.population
        }

class FavoriteCharacter(db.Model):
    __tablename__ = "favoritecharacters"
    id_user= db.Column(db.Integer, ForeignKey("user.id"),primary_key=True)
    user = relationship(User)
    id_character = db.Column(db.Integer, ForeignKey("character.id"),primary_key=True)
    character = relationship(Character)

    def serialize(self):
        return{
        "id_user":self.id_user,
        "id_character":self.id_character

        }

class FavoritePlanet(db.Model):
    __tablename__ = "favoriteplanet"
    id_user= db.Column(db.Integer, ForeignKey("user.id"),primary_key=True)
    user = relationship(User)
    id_planet = db.Column(db.Integer, ForeignKey("planet.id"),primary_key=True)
    planet = relationship(Planet)

    def serialize(self):
        return{
        "id_user":self.id_user,
        "id_planet":self.id_planet

        }

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text, default="")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))

    def serialize(self):
        return{
            "id": self.id,
            "bio":self.bio
        }
    def save(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
