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
from models import db, User, People, Planets, FavoritePeople, FavoritePlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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



##done
@app.route('/people', methods=['GET'])
def list_people():
    people= People.get_peeps()
    serialize_people= [] 
    for people in people: 
        serialize_people.append(people.serialize())
    return jsonify(serialize_people), 200



##done
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person_by_id(people_id):
    people= People.get_people(people_id)
    return jsonify(people.serialize()), 200


##done
@app.route('/planets', methods=['GET'])
def list_planets():
    planets= Planets.get_planets()
    serialize_planets= [] 
    for planet in planets: 
        serialize_planets.append(planet.serialize())
    return jsonify(serialize_planets), 200



##done
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet= Planets.get_by_id(planet_id)
    return jsonify(planet.serialize()), 200

##done
@app.route('/user', methods=['GET'])
def list_users():
    users= User.get_utl()
    serialize_users= [] 
    for user in users: 
        serialize_users.append(user.serialize())
    return jsonify(serialize_users), 200


##done
@app.route('/user/favorites/<int:user_id>', methods=['GET'])
def get_favs(user_id):
    favorites_people= FavoritePeople.query.filter_by(user_id=user_id)
    favorites_planets= FavoritePlanets.query.filter_by(user_id=user_id)
    serialize_favorite= []
    for favorite in favorites_planets: 
        serialize_favorite.append(favorite.serialize())
    return jsonify(serialize_favorite), 200

##done
@app.route('/people/<int:people_id>', methods=['POST'])
def get_people_by_id(people_id):
    people= People.get_people(people_id)
    return jsonify(planet.serialize()), 200

##done
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    dlt= Planets.get_by_id(planet_id)
    return jsonify(dlt.serialize()), 200

##done
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    dlt_people= FavoritePeople.get_fav_people(people_id)
    return jsonify(dlt_people.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
