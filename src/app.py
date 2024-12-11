"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,People,Planet,Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user/<string:username>', methods=['GET'])
def get_users(username=None):
    
    user=User()
    user_true= user.query.filter_by(name=username).first()
   
    if user_true is not None:
        return jsonify({
            "detail":"User already exist"
        }),400
    else:
        user.name=username
        db.session.add(user)
    try:
        db.session.commit()
        return jsonify(user.serialize())
    except Exception as error:
        return jsonify("There is a problem, please try it later or call an admin"),500

@app.route('/people',methods=["POST"])
def add_people():
    
    people=People()
    body = request.json
    
    if body.get("name") is None:
        return jsonify("Debe ingresar un nombre"),400
    
    if body.get("age") is None:
        return jsonify("Debe ingresar la edad"),400
    
    if body.get("eye_color") is None:
        return jsonify("Debe ingresar el color de ojos"),400
    
    if body.get("skin_color") is None:
        return jsonify("Debe ingrear el color"),400
    
    people.name= body["name"]
    people.age = body["age"]
    people.eye_color = body["eye_color"]
    people.skin_color=body["skin_color"]

    db.session.add(people)

    try:
        db.session.commit()
        return jsonify(people.serialize_people()),201
    except Exception as err:
        print(err.args)
        return jsonify(err.args)

@app.route('/planet', methods=["POST"])
def add_planet():

    try:
        planet=Planet()
        body= request.json
        if body.get("name") is None:
            return jsonify("Debe ingresar el nombre"),400
        if body.get("climate") is None:
            return jsonify("Debe ingresar el clima"),400
        if body.get("gravity")is None:
            return jsonify("Debe ingresar la gravedad"),400
        
        planet.name = body["name"]
        planet.climate = body["climate"]
        planet.gravity = body["gravity"]

        db.session.add(planet)
        try:
            db.session.commit()
            return jsonify(planet.serialize_planet()),201
        except Exception as error:
            return jsonify(error.args)
    except Exception as err:
        print(err.args)
        return jsonify("Error"),500


@app.route('/people', methods=["GET"])
def get_people():

    try:
        people=People.query.all()
        if people is None:
            return jsonify({
                "detail": "This character doesn't exist"
            }),400
        else:
            people= list(map(lambda item:item.serialize(),people))
            return jsonify(people),200
    except Exception as err:
        print(err.args)
        return jsonify("Error"),500
    
@app.route('/people/<int:people_id>', methods=["GET"])
def get_one_character(people_id):
    
    try:
        character= People.query.get(people_id)

        if character is None:
            return jsonify(f'El id {people_id} no se encontor'),400
        else:
            character=character.serialize()
            return jsonify(character),200
    except Exception as err:
        print(err.args)
        return jsonify("Error"),500

@app.route('/planet' , methods=["GET"])
def get_planets():
    try:
        planets = Planet.query.all()
        if planets is None:
            return jsonify({
                "detail":"This planet doesn't exist"
            }),400
        else:
            planets=list(map(lambda item:item.serialize(), planets))
    except Exception as err:
        print(err.args)
        return jsonify("Error"),500

@app.route('/planets/<int:planet_id>', methods=["GET"])
def get_one_planet(planet_id):

    try:
        planet= Planet.query.get(planet_id)

        if planet is None:
            return jsonify({
                "detail":f"The planet{planet_id} doesn't exist"
            })
        else:
            planet = planet.serialize()
            return jsonify(planet),200
    except Exception as err:
        print(err.args)
        return jsonify("Error"),500

@app.route('/users/favorites', methods=["GET"])
def user_favorites():
    try:
        favorites=Favorite.query.all()
        return jsonify(list(map(lambda item:item.serialize(), favorites)))
    except Exception as err:
        print(err.args)
        return jsonify("Error"),500

@app.route('/favorite/planet/<int:planet_id>', methods=["POST"])
def add_planet_favorite(planet_id):
    try:
        body= request.json
        fav=Favorite()
        fav.user_id=body["user_id"]
        fav.planet_id=planet_id

        db.session.add(fav)
        db.session.commit()

        return jsonify("Se añadio exitosamente"),200    
    except Exception as err:
        print(err.args)
        return jsonify("Error"),500


@app.route('/favorite/people/<int:people_id>', methods=["POST"])
def add_favorite_people(people_id):
    try:
        body = request.json
        fav = Favorite()
        fav.user_id=body["user_id"]
        fav.people_id=people_id

        db.session.add(fav)
        db.session.commit

    except Exception as err:
        print(err.args)
        return jsonify("Error"),500
    
@app.route('/favorite/planet/<int:planet_id>', methods=["DELETE"])
def delete_favorite_planet(planet_id):
    try:
        fav_delete = Favorite.query.get(planet_id)
        if fav_delete is None:
            return jsonify(f"The planet with the id{planet_id} doesn't exist"),400
        else:
            db.session.delete(fav_delete)
            db.session.commit()
            return jsonify([]),204
    except Exception as err:
        print(err.args)
        return jsonify("Error"), 500

@app.route('/favorite/people/<int:people_id>', methods=["DELETE"])
def delete_favorite_people(people_id):
    try:
        fav_delete=Favorite.query.get(people_id)
        if fav_delete is None:
            return jsonify(f"the character with the id {people_id} doesn't exist"),400
        else:
            db.session.add(fav_delete)
            db.session.commit()
            return jsonify([]),202
    except Exception as err:
        print(err.args)
        return jsonify("Error"),500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
