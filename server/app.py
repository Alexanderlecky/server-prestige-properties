import os
from flask import Flask, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from config import Config  # Importing configuration
from models import db, User, House, Favorite  # Importing models
from dotenv import load_dotenv
from  flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Initialize Flask and its extensions
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)  # Load configurations from Config class
CORS(app)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

# Create database tables
with app.app_context():
    db.create_all()

# Load user for Flask-Login session management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ Authentication Endpoints ------------------

# POST: Sign up
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "User with that email or username already exists"}), 400

# POST: Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# ------------------ Property Endpoints ------------------

# GET: Retrieve all properties (no login required)
@app.route('/properties', methods=['GET'])
def get_properties():
    houses = House.query.all()
    return jsonify([{
        "id": house.id,
        "name": house.name,
        "description": house.description,
        "location": house.location,
        "price": house.price,
        "image": house.image,
    } for house in houses]), 200

# GET: Retrieve a specific property (no login required)
@app.route('/properties/<int:house_id>', methods=['GET'])
def get_property(house_id):
    house = House.query.get_or_404(house_id)
    return jsonify({
        "id": house.id,
        "name": house.name,
        "description": house.description,
        "location": house.location,
        "price": house.price,
        "image": house.image,
    }), 200

# PUT: Update property details (login required)
@app.route('/properties/<int:house_id>', methods=['PUT'])
@login_required
def update_property(house_id):
    house = House.query.get_or_404(house_id)
    data = request.get_json()

    house.name = data.get('name', house.name)
    house.description = data.get('description', house.description)
    house.location = data.get('location', house.location)
    house.price = data.get('price', house.price)

    db.session.commit()
    return jsonify({"message": "Property updated successfully"}), 200

# ------------------ Favorite Endpoints ------------------

# POST: Add a property to favorites (login required)
@app.route('/favorites/add/<int:house_id>', methods=['POST'])
@login_required
def add_favorite(house_id):
    favorite = Favorite(user_id=current_user.id, house_id=house_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Added to favorites"}), 201

# GET: Retrieve all favorites for the logged-in user (login required)
@app.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        "id": fav.house.id,
        "name": fav.house.name,
        "location": fav.house.location,
        "price": fav.house.price,
        "image": fav.house.image
    } for fav in favorites]), 200

# PATCH: Update a favorite (login required)
@app.route('/favorites/<int:favorite_id>', methods=['PATCH'])
@login_required
def update_favorite(favorite_id):
    favorite = Favorite.query.get_or_404(favorite_id)

    if favorite.user_id != current_user.id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    # Assume we allow patching notes (or other favorite-related info)
    favorite.notes = data.get('notes', favorite.notes)
    db.session.commit()
    return jsonify({"message": "Favorite updated successfully"}), 200

# DELETE: Remove a favorite (login required)
@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
@login_required
def delete_favorite(favorite_id):
    favorite = Favorite.query.get_or_404(favorite_id)

    if favorite.user_id != current_user.id:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite removed successfully"}), 200

# ------------------ Run Application ------------------
if __name__ == "__main__":
    app.run(debug=True)
