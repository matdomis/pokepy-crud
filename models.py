from flask_login import UserMixin #type: ignore
from datetime import datetime

from app import db

class User(db.Model, UserMixin):
    """
        Represents a user in the application.

        Inherits from SQLAlchemy's 'db.Model' and Flask-Login's 'UserMixin' for ORM functionality
        and session management.

        Attributes:
            uid (int): Unique identifier for the user (Primary Key).
            username (str): The username of the user (must be unique and not null).
            password (str): The hashed password of the user (cannot be null).
            gender (bool): Gender of the user (True for male, False for female).
            created_at (datetime): Timestamp of when the user account was created (defaults to the current time).
            pokemons (relationship): A one-to-many relationship with the `Pokemon` model, linking each user to their Pokémon.

        Methods:
            __repr__(): Returns a string representation of the user instance, including the user ID and username.
            get_id(): Returns the user's unique ID for use with Flask-Login session management.
    """

    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    pokemons = db.relationship('Pokemon', backref='owner', lazy=True)

    def __repr__(self):
        return f"<{self.uid}> {self.username}"
    
    def get_id(self):
        return self.uid


class Pokemon(db.Model):
    """
        Represents a Pokémon in the application.

        Inherits from SQLAlchemy's 'db.Model' for ORM functionality.

        Attributes:
            id (int): Unique identifier for the Pokémon (Primary Key).
            pokemon_name (str): Name of the Pokémon (cannot be null).
            user_id (int): Foreign key linking the Pokémon to a user (cannot be null, references `users.uid`).
            added_at (datetime): Timestamp of when the Pokémon was added to the user's collection (defaults to the current time).

        Methods:
            __repr__(): Returns a string representation of the Pokémon instance, including the Pokémon ID.
    """
    
    __tablename__ = 'pokemons'

    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Pokemon {self.pokeapi_id}>"