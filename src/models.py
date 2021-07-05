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
    favoChas = db.relationship("FavoriteCharacter", cascade="all, delete", backref="favocha")


    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "password":self.password,
            "bio":self.profile.serialize(),
            "favorite_characters":self.get_characters()
        }
    
    def get_characters(self):
        characters = list(map(lambda cha : cha.serialize(), self.favoChas))
        return characters
    
    def darNombre(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


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
    favoCha = db.relationship("FavoriteCharacter", cascade="all, delete", backref="character")

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
    def darNombre(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class FavoriteCharacter(db.Model):
    __tablename__ = "favoritecharacters"
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id", ondelete="CASCADE"), nullable=False)
    

    # def serialize_with_name_character(self):
    #     return{
    #         "name":self.favoritecha.name
    #     }
    def serialize(self):
        return{
        # "user_id":self.user_id,
        # "character_id":self.character_id,
        "name":self.character.name,
        
        }
    
    




class FavoritePlanet(db.Model):
    __tablename__ = "favoriteplanet"
    user_id= db.Column(db.Integer, ForeignKey("user.id"),primary_key=True)
    user = relationship(User)
    id_planet = db.Column(db.Integer, ForeignKey("planet.id"),primary_key=True)
    planet = relationship(Planet)

    def serialize(self):
        return{
        "user_id":self.user_id,
        "id_planet":self.id_planet,
        

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
