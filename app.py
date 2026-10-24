from typing import List
from urllib.parse import urlencode

from flask import Flask, render_template, request, jsonify
from data import (
    get_all_games,
    get_pokemon_info_by_name,
    get_locations_by_region,
    get_areas_by_location,
    get_region_by_game,
    EncounterMethods,
    get_encounter_by_area_filtered_methods,
    get_encounter_info_by_pokemon,
)

app = Flask(__name__)


def format_name(value):
    if value is None:
        return ""
    return " ".join(part.capitalize() for part in str(value).replace('-', ' ').split())

def test_get_pokemon_list_by_game(game_str: str) -> List[str]:
    # This is a placeholder for the actual implementation.
    # Replace this with the actual logic to retrieve the list of Pokémon names for the given game.
    if game_str == "red" or game_str == "blue":
        return ["Pikachu", "Charmander", "Bulbasaur", "Squirtle"]
    else:
        return ["Unknown Pokémon"]

def test_get_pokemon_data(pokemon_name: str) -> dict:
    # This is a placeholder for the actual implementation.
    # Replace this with the actual logic to retrieve Pokémon data by name.
    if pokemon_name.lower() == "pikachu":
        return {
            "name": "Pikachu",
            "type": ["Electric"],
            "base_stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
            "abilities": ["Static", "Lightning Rod"],
        }
    else:
        placeholder_data = {
            "name": pokemon_name,
            "type": ["Normal"],
            "base_stats": {"hp": 50, "attack": 50, "defense": 50, "special_attack": 50, "special_defense": 50, "speed": 50},
            "abilities": ["Run Away", "Adaptability"],
        }
        return placeholder_data

app.jinja_env.filters['format_name'] = format_name

@app.route('/') 
@app.route('/index')
def index():
    user = {'username': 'Nick'}
    favorites = [
        {'pokemon_name': 'Bisasam', 'reason': 'Goat Pokémon'},
        {'pokemon_name': 'Zorua', 'reason': 'Cute as Fuck'},
    ]
    return render_template('index.html', title='PokeRandom', user=user, favorites=favorites)


@app.route('/selection')
def selection():
    games = get_all_games()
    encounter_methods = EncounterMethods
    return render_template('selection.html', games=games, encounter_methods=encounter_methods)


@app.route('/result')
def result():
    # Raw values -- these are exactly what the /api/* endpoints expect,
    # and what we hand back to /selection so it can restore the choice.
    game = request.args.get('game')
    region = request.args.get('region')
    location = request.args.get('location')
    area_number = request.args.get('area_number', type=int)
    methods = request.args.getlist('method')
    min_level = request.args.get('min_level', type=int)
    max_level = request.args.get('max_level', type=int)

    # Display-only text -- only used to render the summary chips on this page.
    region_name = request.args.get('region_name')
    location_name = request.args.get('location_name')
    area_name = request.args.get('area_name')
    pokemon_name = request.args.get('pokemon_name')

    pokemon_data = get_pokemon_info_by_name(game_str = game, pokemon_name = pokemon_name, area_num = area_number)

    if min_level is None or max_level is None:
        encounter_levels = [
            level
            for encounter in pokemon_data.get('encounters', [])
            for level in [encounter.get('min_level'), encounter.get('max_level')]
            if level is not None
        ]
        if encounter_levels:
            min_level = min(encounter_levels)
            max_level = max(encounter_levels)

    # Build the query string for "Back to selection" so the raw
    # game/region/location/area/method choices can be replayed there.
    back_query_params = [
        ('game', game),
        ('region', region),
        ('location', location),
        ('area_number', area_number),
    ]
    back_query_params += [('method', m) for m in methods]
    back_query = urlencode(back_query_params)

    return render_template(
        'result.html',
        game=game,
        region_name=region_name,
        location_name=location_name,
        area_name=area_name,
        pokemon_data=pokemon_data,
        min_level=min_level,
        max_level=max_level,
        back_query=back_query
    )

@app.route('/damage_calculator')
def damage_calculator():
    games = get_all_games()
    return render_template('damage-calc.html', games=games)


# --- API routes (return JSON, called by fetch() in the browser) -----------

@app.route('/api/locations')
def api_locations():
    region = request.args.get('region', type=str)
    if region is None:
        return jsonify([])

    locations : list[dict[str, str]] = get_locations_by_region(region)
    return jsonify(locations)


@app.route('/api/areas')
def api_areas():
    location_number = request.args.get('location', type=int)
    if not location_number:
        return jsonify([])

    areas = get_areas_by_location(location_number)
    return jsonify(areas)

@app.route('/api/encounters')
def api_encounters():
    area = request.args.get('area', type=int)
    game_str = request.args.get('game', type=str)
    encounter_methods = request.args.getlist('method')
    if not area:
        return jsonify([])

    encounters = get_encounter_by_area_filtered_methods(area, game_str, encounter_methods)

    for encounter in encounters:
        details = get_encounter_info_by_pokemon(area, game_str, encounter['name'])
        levels = [
            level
            for info in details
            for level in [info.get('min_level'), info.get('max_level')]
            if level is not None
        ]
        if levels:
            encounter['min_level'] = min(levels)
            encounter['max_level'] = max(levels)
        else:
            encounter['min_level'] = None
            encounter['max_level'] = None

    return jsonify(encounters)

@app.route('/api/regions')
def api_regions():
    game_name = request.args.get('game', type=str)
    if not game_name:
        return jsonify([])
    regions : list[str] = get_region_by_game(game_name)
    return regions

@app.route('/api/pokemon_list')
def api_pokemon_list():
    game_name = request.args.get('game', type=str)
    if not game_name:
        return jsonify([])

    pokemon_list = test_get_pokemon_list_by_game(game_name)
    return jsonify(pokemon_list)

@app.route('/api/pokemon_data')
def api_pokemon_data():
    pokemon_name = request.args.get('name', type=str)
    if not pokemon_name:
        return jsonify({})

    pokemon_data = test_get_pokemon_data(pokemon_name)
    return jsonify(pokemon_data)

if __name__ == '__main__':
    app.run(debug=True)