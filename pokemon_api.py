import requests

ACCEPTED = 200

def get_pokemon_json(pokemon_name: str) -> dict:
    """
    Get the pokemon data from the PokeAPI and returns a JSON
    """
    
    try:
        pokemon_name = pokemon_name.lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        
        if response.status_code == ACCEPTED:
            data = response.json()

            return {
                'name': data['name'],
                'height': data['height'],
                'weight': data['weight'],
                'types': [
                        f"https://play.pokemonshowdown.com/sprites/types/{t['type']['name'].capitalize()}.png"
                        for t in data['types']
                    ],
                'sprite': data['sprites']['front_default']
            }        
    
    except Exception as e:
        print(f'Request from the PokeAPI failed: {str(e)}')
    
    return None

