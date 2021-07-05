from operator import ge
from os import access, name
from typing import BinaryIO
from flask import Flask, jsonify, request, render_template
from flask_migrate import Migrate
from models import Profile, db,User,Character,FavoriteCharacter,Planet, FavoritePlanet, Profile
#import from jwt doc
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///datastar.db"

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "use-super-token"  # Change this!
jwt = JWTManager(app)

db.init_app(app)
Migrate(app,db)


#Ruta para login
@app.route("/login", methods=["POST"])
def login():
    name = request.json.get("name", None)
    password = request.json.get("password", None)
    #Search the current user in the db
    user = User.query.filter_by(name = name, password=password).first()
    if user is None:
        #Return that the user is not in db
        return jsonify({"msg":"User or password incorrect"}), 401
    # si esta, create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "user_id":user.id})

""" #Ruta para proteger
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    #Acceder ala identidad del usuario actual con get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    return jsonify({"id": user.id, "username":user.name}),200 """
    


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")
""" #GET PARA USER
@app.route("/api/users", methods=["GET"])
def list_user():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(),users))
    return jsonify(users), 200

""" 
#GET SINGLE USER
@app.route("/api/user", methods=["GET"])
@jwt_required()

def get_single_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    

    return jsonify(user.serialize()), 200 

#GET Characters favoritos de un user
@app.route("/api/favoritos", methods=["GET"])
@jwt_required()

def get_favoritos_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    

    return jsonify(user.name, user.get_characters()), 200

""" #POST PARA USER
@app.route("/api/users",methods = ["POST"])
def post_user():
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")

    bio = request.json.get("bio", "")

    user = User()
    user.name = name
    user.email = email
    user.password = password

    profile = Profile()
    profile.bio = bio

    user.profile = profile



    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 201 """
#GET;POST UPDATE DELETE USER
@app.route("/api/users", methods=["GET","POST"])
@app.route("/api/users/<int:id>", methods=["GET","DELETE","PUT"])

def users(id=None):
    if request.method == "GET":
        if id is not None:
            user = User.query.get(id)
            return jsonify(user.serialize()), 200
    
        users = User.query.all()
        users = list(map(lambda user: user.serialize(), users))
        return jsonify(users), 200

    if request.method == "POST":
        name = request.json.get("name")
        email = request.json.get("email")
        password = request.json.get("password")

        bio = request.json.get("bio", "")
        

        user = User()
        user.name = name
        user.email = email
        user.password = password

        profile = Profile()
        profile.bio = bio

        user.profile = profile
        user.save()

        return jsonify(user.serialize()), 201
    
    if request.method == "PUT":
        name = request.json.get("name")
        email = request.json.get("email")
        password = request.json.get("password")

        bio = request.json.get("bio", "")

        user = User.query.get(id)
        user.name = name
        user.email = email
        user.password = password
        user.profile.bio = bio #relationship

        profile = Profile.query.filter_by(user_id =id).first()
        

        user.profile = profile

        user.update()

        return jsonify(user.serialize()), 200
    
    if request.method == "DELETE":
        user = User.query.get(id)
        user.delete()
        return jsonify({"Success":"User Eliminated"})

       

""" #GET PARA CHARACTERS
@app.route("/api/characters", methods = ["GET"])
def list_character():
    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(),characters))

    return jsonify(characters), 200

#POST PARA CHARACTERS
@app.route("/api/characters", methods=["POST"])
def post_character():
    name = request.json.get("name")
    height = request.json.get("height")
    mass = request.json.get("mass")
    hair_color = request.json.get("hair_color")
    skin_color = request.json.get("skin_color")
    eye_color = request.json.get("eye_color")
    birth_year = request.json.get("birth_year")
    gender = request.json.get("gender")
    homeworld = request.json.get("homeworld")
    character = Character()
    character.name = name
    character.height = height
    character.mass= mass
    character.hair_color = hair_color
    character.skin_color = skin_color
    character.eye_color = eye_color
    character.birth_year = birth_year
    character.gender = gender
    character.homeworld = homeworld

    

    db.session.add(character)
    db.session.commit()

    return jsonify(character.serialize()), 201 """

#GET ; POST PUT; DELETER PARA CHARACTERS

@app.route("/api/characters",methods=["GET","POST"])
@app.route("/api/characters/<int:id>", methods = ["GET","PUT","DELETE"])
def _characters(id = None):
    if request.method == "GET":
        if id is not None:
            character = Character.query.get(id)
            return jsonify(character.serialize()),200
        
        characters = Character.query.all()
        characters = list(map(lambda character : character.serialize(),characters))
        return jsonify(characters), 200
    if request.method == "POST":
        name = request.json.get("name")
        height = request.json.get("height")
        mass = request.json.get("mass")
        hair_color = request.json.get("hair_color")
        skin_color = request.json.get("skin_color")
        eye_color = request.json.get("eye_color")
        birth_year = request.json.get("birth_year")
        gender = request.json.get("gender")
        homeworld = request.json.get("homeworld")
        character = Character()
        character.name = name
        character.height = height
        character.mass= mass
        character.hair_color = hair_color
        character.skin_color = skin_color
        character.eye_color = eye_color
        character.birth_year = birth_year
        character.gender = gender
        character.homeworld = homeworld
        character.save()

        return jsonify(character.serialize()),201

    if request.method == "PUT":
        name = request.json.get("name")
        height = request.json.get("height")
        mass = request.json.get("mass")
        hair_color = request.json.get("hair_color")
        skin_color = request.json.get("skin_color")
        eye_color = request.json.get("eye_color")
        birth_year = request.json.get("birth_year")
        gender = request.json.get("gender")
        homeworld = request.json.get("homeworld")
        character = Character.query.get(id)
        character.name = name
        character.height = height
        character.mass= mass
        character.hair_color = hair_color
        character.skin_color = skin_color
        character.eye_color = eye_color
        character.birth_year = birth_year
        character.gender = gender
        character.homeworld = homeworld
        character.update()

        return jsonify(character.serialize()), 200
    if request.method == "DELETE":
        character = Character.query.get(id)
        character.delete()
        return jsonify({"Success":"Character Deleted"}), 200

#GET FAVORITE CHARACTER
@app.route("/api/favoriteCharacters")
def list_favorite_characters():
    favoritesCh = FavoriteCharacter.query.all()
    
    favoritesCh = list(map(lambda favo : favo.serialize(),favoritesCh))


    return jsonify(favoritesCh), 200

#POST FAVORITE CHARACTER
@app.route("/api/favoriteCharacters", methods = ["POST"])
def post_favorite_character():
    user_id = request.json.get("user_id")
    character_id = request.json.get("character_id")
    favoriteCh = FavoriteCharacter()
    favoriteCh.user_id = user_id
    favoriteCh.character_id = character_id

    db.session.add(favoriteCh)
    db.session.commit()

    return jsonify(favoriteCh.serialize()), 201

#GET FAVORITE PLANET
@app.route("/api/favoritePlanets", methods=["GET"])
def get_favorite_planets():
    favoritePl = FavoritePlanet.query.all()
    favoritePl = list(map(lambda favo: favo.serialize(),favoritePl))

    return jsonify(favoritePl), 200

#POST FAVORITE PLANETS
@app.route("/api/favoritePlanets", methods=["POST"])
def post_favorite_planets():
    user_id = request.json.get("user_id")
    id_planet = request.json.get("id_planet")
    favoritePl = FavoritePlanet()
    favoritePl.user_id = user_id
    favoritePl.id_planet = id_planet

    db.session.add(favoritePl)
    db.session.commit()

    return jsonify(favoritePl.serialize()),201

#POST.GET.UPDATE.DELETE PLANETS
@app.route("/api/planets", methods=["GET","POST"])
@app.route("/api/planets/<int:id>" ,methods=["GET","PUT","DELETE"])
def planets(id = None):
    if request.method == "GET":
        if id is not None:
            planet = Planet.query.get(id)
            return jsonify(planet.serialize()), 200
        
        planets = Planet.query.all()
        planets = list(map(lambda planet : planet.serialize(),planets))
        return jsonify(planets),200
    
    if request.method == "POST":
        
        name = request.json.get("name")
        diameter = request.json.get("diameter")
        climate = request.json.get("climate")
        gravity = request.json.get("gravity")
        terrain = request.json.get("terrain")
        population = request.json.get("population")

        planet = Planet()
        planet.name = name
        planet.diameter =diameter
        planet.climate = climate
        planet.gravity = gravity
        planet.terrain = terrain
        planet.population = population

        planet.save()
        
        return jsonify(planet.serialize()),201
    
    if request.method == "PUT":
        name = request.json.get("name")
        diameter = request.json.get("diameter")
        climate = request.json.get("climate")
        gravity = request.json.get("gravity")
        terrain = request.json.get("terrain")
        population = request.json.get("population")

        planet = Planet.query.get(id)
        planet.name = name
        planet.diameter =diameter
        planet.climate = climate
        planet.gravity = gravity
        planet.terrain = terrain
        planet.population = population

        planet.update()

        return jsonify(planet.serialize()), 200
    
    if request.method == "DELETE":
        planet = Planet.query.get(id)
        planet.delete()

        return jsonify({"Success": "Planet Eliminated"}), 200






#Iniciar ,,, Siempre esto al final
if(__name__ == "__main__"):
    app.run()