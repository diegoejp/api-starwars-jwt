from operator import ge
from flask import Flask, jsonify, request, render_template
from flask_migrate import Migrate
from models import Profile, db,User,Character,FavoriteCharacter,Planet, FavoritePlanet, Profile

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///datastar.db"

db.init_app(app)
Migrate(app,db)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")
#GET PARA USER
@app.route("/api/users", methods=["GET"])
def list_user():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(),users))
    return jsonify(users), 200

#GET SINGLE USER
@app.route("/api/users/<int:id>", methods=["GET"])
def get_single_user(id):
    user = User.query.get(id)

    return jsonify(user.serialize()), 200

#POST PARA USER
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

    return jsonify(user.serialize()), 201

#GET PARA CHARACTERS
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

    return jsonify(character.serialize()), 201

#GET FAVORITE CHARACTER
@app.route("/api/favoriteCharacters")
def list_favorite_characters():
    favoritesCh = FavoriteCharacter.query.all()
    favoritesCh = list(map(lambda favo : favo.serialize(),favoritesCh))

    return jsonify(favoritesCh), 200

#POST FAVORITE CHARACTER
@app.route("/api/favoriteCharacters", methods = ["POST"])
def post_favorite_character():
    id_user = request.json.get("id_user")
    id_character = request.json.get("id_character")
    favoriteCh = FavoriteCharacter()
    favoriteCh.id_user = id_user
    favoriteCh.id_character = id_character

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
    id_user = request.json.get("id_user")
    id_planet = request.json.get("id_planet")
    favoritePl = FavoritePlanet()
    favoritePl.id_user = id_user
    favoritePl.id_planet = id_planet

    db.session.add(favoritePl)
    db.session.commit()

    return jsonify(favoritePl.serialize()),201




#Iniciar ,,, Siempre esto al final
if(__name__ == "__main__"):
    app.run()