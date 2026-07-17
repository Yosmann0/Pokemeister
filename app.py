from flask import Flask, render_template, request, jsonify
from data import get_all_games, get_pokemon_info_by_name, get_locations_by_region, get_areas_for_location, get_encounter_for_area, get_region_by_game

app = Flask(__name__)

def get_generations():
    return [1, 2, 3, 4, 5, 6, 7, 8]


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
    return render_template('selection.html', games=games)


@app.route('/result')
def result():
    game = request.args.get('game')
    region = request.args.get('region')
    location = request.args.get('location')
    area = request.args.get('area')
    pokemon_name = request.args.get('pokemon_name')

    pokemon_data = get_pokemon_info_by_name(pokemon_name)

    return render_template(
        'result.html',
        game=game,
        region=region,
        location=location,
        area=area,
        pokemon_data=pokemon_data
    )


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

    areas = get_areas_for_location(location_number)
    return jsonify(areas)

@app.route('/api/encounters')
def api_encounters():
    area_number = request.args.get('area', type=int)
    if not area_number:
        return jsonify([])

    encounters = get_encounter_for_area(area_number)
    return jsonify(encounters)

@app.route('/api/regions')
def api_regions():
    game_name = request.args.get('game', type=str)
    if not game_name:
        return jsonify([])
    regions : list[str] = get_region_by_game(game_name)
    return regions

if __name__ == '__main__':
    app.run(debug=True)