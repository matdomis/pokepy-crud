from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required           #type: ignore
import random

from pokemon_api import get_pokemon_json
from models import User, Pokemon

def generate_views(app, db, bcrypt):
    """
        Registers all Flask view routes (endpoints) to the given Flask application.
    """

    @app.route('/', methods=['GET', 'POST'])
    def login():
        """
            Handle user login.

            - If the user is already authenticated, they are logged out to ensure a fresh login.
            - On a POST request, the function checks submitted credentials against the database.
            - If the username and password match, the user is logged in and redirected to the dashboard.
            - If authentication fails, appropriate flash messages are shown.
            - On a GET request, or after failed login, the login page is rendered.
        """

        try:
            if current_user.is_authenticated:
                logout_user()

            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')

                user = User.query.filter(User.username == username).first()

                if user:
                    if bcrypt.check_password_hash(user.password, password):
                        login_user(user)
                        return redirect(url_for('dashboard'))
                    else:
                        flash('Wrong password')
                else:
                    flash('Username not found')
        except Exception as e:
            return str(e)

        return render_template('login.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        """
            Handle user registration.

            - If a user is already authenticated, they are logged out to prevent conflicts.
            - On a POST request:
                - Retrieves and validates submitted form data (username, password, password confirmation, gender).
                - Ensures passwords match and that the username is not already registered.
                - Hashes the password and creates a new user in the database.
                - Displays appropriate flash messages for errors or successful registration.
                - Redirects to the login page on successful registration.
            - On a GET request (or after a failed POST), renders the signup page along with the total user count.
         """

        users_counter = db.session.query(User).count()

        try:
            if current_user.is_authenticated:
                logout_user()
        
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                confirm_password = request.form.get('confirm-password')
                gender = request.form.get('gender')
                
                gender = True if gender == 'male' else False

                if password != confirm_password:
                    flash('Passwords dont match!')
                    return render_template('signup.html', users_counter=users_counter)
                
                user = User.query.filter(User.username == username).first()
                if user:
                    flash('Username already exists in our database!')
                    return render_template('signup.html', users_counter=users_counter)

                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                new_user = User(username=username, password=hashed_password, gender=gender)

                db.session.add(new_user)
                db.session.commit()
                flash('User created successfully!')
                return redirect(url_for('login'))
        except Exception as e:
            return str(e)

        return render_template('signup.html', users_counter=users_counter)

    @app.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():   
        """
            Handle the user dashboard view and Pokémon registration.

            - Requires the user to be authenticated.

            - On a POST request:
                - Expects a JSON payload containing a Pokémon name.
                - Attempts to retrieve Pokémon data from PokeAPI.
                - If the Pokémon exists:
                    - Saves it to the database for the current user.
                    - Renders a partial HTML card for the Pokémon and returns it in a JSON response.
                - If not found, returns a JSON error with a 404 status to JavaScript.

            - On a GET request:
                - Fetches all Pokémon registered by the current user.
                - Retrieves their data and adds their database ID to the payload.
                - Renders the full dashboard page with all the user's Pokémon as cards.
        """

        try:
            if request.method == 'POST':
                data = request.get_json()
                pokemon_name = data.get('name').lower()

                pokemon_data = get_pokemon_json(pokemon_name)

                if pokemon_data:

                    new_pokemon = Pokemon(pokemon_name=pokemon_name, user_id=current_user.uid)

                    db.session.add(new_pokemon)
                    db.session.commit()
                    
                    # Add the 'id' (number line in the table Pokemon) to pokemon_data to identify each card -- important for delete function afterwards.
                    pokemon_data['id'] = new_pokemon.id                                 

                    rendered_card = render_template('partials/card.html', pokemon=pokemon_data)
                    return jsonify( {'html': rendered_card} ), 200
                
                return jsonify( {'error': 'Error: Pokemon not found!'} ), 404
       
        except Exception as e:
            return jsonify( {'error': str(e)} ), 500
        
        # Returns a list instance, each element of the list is an object Pokemon()
        pokemons = Pokemon.query.filter(Pokemon.user_id == current_user.uid).all()
        pokemons_card = []
        for poke in pokemons:
            pokemon_data = get_pokemon_json(poke.pokemon_name)

            # Add the 'id' (number line in the table Pokemon) to pokemon_data to identify each card -- important for delete function afterwards.
            pokemon_data['id'] = poke.id    

            pokemons_card.append(pokemon_data)

        return render_template('dashboard.html', pokemons_card=pokemons_card)      




    @app.route('/delete_pokemon/<int:id>', methods=['DELETE'])
    def delete_pokemon(id):
        """
            Handle deletion of a Pokémon by its database ID.

            - Accepts a DELETE request with the Pokémon's ID as a URL parameter.
            - Attempts to find the corresponding Pokémon in the database.
                - If found, deletes the record and commits the change.
                - Returns a success message in JSON format.
            - If an exception occurs during the process, returns a 500 error with the exception message.
            - If no exception occurs but the Pokémon was not properly handled, returns a generic error message.
        """

        try:
            pokemon = Pokemon.query.get(id)
            if pokemon:
                db.session.delete(pokemon)
                db.session.commit()
                return jsonify( {'message': 'Pokemon has been deleted successfully!'}), 200
        except Exception as e:
            return jsonify( {'error': str(e)} ), 500
    
        return jsonify( {'error': 'Some error has been ocurred while deleting this pokemon.'}), 404


    @app.route('/random_pokemon', methods=['POST'])
    def random_pokemon():
        """
            Generate and register a random Pokémon for the current user.

            - Selects a random Pokémon ID between 1 and 1025 (Number of the last pokemon in the Poke-Dex :D ).
            - Fetches the Pokémon's data using PokeAPI.
            - If valid data is returned:
                - Extracts the name and creates a new Pokémon entry for the current user.
                - Commits the new Pokémon to the database.
                - Renders a partial HTML card for the Pokémon and returns it in a JSON response.
            - If an exception occurs during processing, returns a 500 error with the exception message.
        """
        
        random_id = random.randint(1, 1025)
        random_id = str(random_id)
        
        try:
            pokemon_data = get_pokemon_json(random_id)

            if pokemon_data:
                pokemon_name = pokemon_data['name']

                new_pokemon = Pokemon(pokemon_name=pokemon_name, user_id=current_user.uid)

                db.session.add(new_pokemon)
                db.session.commit()

                # Add the 'id' (number line in the table Pokemon) to pokemon_data to identify each card -- important for delete function afterwards.
                pokemon_data['id'] = new_pokemon.id

                rendered_card = render_template('partials/card.html', pokemon=pokemon_data)
                return jsonify( {'html': rendered_card} ), 200
        
        except Exception as e:
            return jsonify( {'error': str(e)} ), 500


    @app.route('/clear_pokemon', methods=['POST'])
    def clear_pokemon():
        """
            Delete all Pokémon associated with the currently logged-in user.

            - Accepts a POST request.
            - Filters and deletes all Pokémon entries in the database linked to the current user's ID.
            - Commits the deletion and returns a message indicating how many records were removed.
            - If an exception occurs, rolls back the transaction and returns a 500 error with the exception message.

        """
        
        try:
            delete_count = Pokemon.query.filter(Pokemon.user_id == current_user.uid).delete()
            db.session.commit()
            return jsonify( {"message": f"{delete_count} Pokémons deleted successfully."}), 200
        
        except Exception as e:
            db.session.rollback()
            return jsonify( {"error": str(e)} ), 500

    @app.route('/logout', methods=['GET'])
    def logout():
        """
            Log out the current user and redirect to the login page.
        """

        logout_user()
        return redirect(url_for('login'))