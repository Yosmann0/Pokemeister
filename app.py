from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


def get_generations():
    return [1, 2, 3, 4, 5, 6, 7, 8]

def get_pokemon_data(pokemon_name):
    print(f"DEBUG: get_pokemon_data({pokemon_name}) called")

    if pokemon_name == "pikachu":
        return {
            'name': 'pikachu',
            'stats': {'HP': 35, 'ATK': 55, 'DEF': 40, 'SPEATK': 50, 'SPEDEF': 50, 'SPE': 90, 'BST': 320},
            'id': 25, 
            'typing': {'electric'}, 
            'species': 'pikachu', 
            'pokewiki_url': 'https://www.pokewiki.de/pikachu', 
            'height': 4, 'weight': 60, 'sprite': 
            'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'
            }

    else:
        print(f"DEBUG: get_pokemon_data({pokemon_name}) -> Pokemon not found")
        return {}

def get_locations_for_generation(generation):
    locations_by_generation = {
        1: {"location-1": "1", "location-2": "2", "location-3": "3"},
        2: {"location-4": "4", "location-5": "5"},
        3: {"location-6": "6", "location-7": "7"},
    }
    locations = locations_by_generation.get(generation, {"Unknown Location": "unknown_url"})

    result = [{"name": name, "id": number} for name, number in locations.items()]
    print(f"DEBUG: get_locations_for_generation({generation}) -> {result}")
    return result


def get_areas_for_location(location_number):
    areas_by_location = {
        1: {"area1": "1", "area2": "2", "area3": "3"},
        2: {"area1": "4", "area2": "5"},
        3: {"area1": "6", "area2": "7"},
    }
    areas = areas_by_location.get(location_number, {"empty_area1": "1"})

    result = [{"name": name, "id": url} for name, url in areas.items()]
    print(f"DEBUG: get_areas_for_location({location_number}) -> {result}")
    return result


def get_encounter_by_area(area_number):
    encounter_by_area = {
        1: {"pikachu": "p_url1", "pokemon2": "p_url2", "pokemon3": "p_url3"},
        2: {"pokemon1": "p_url4", "pokemon2": "p_url5"},
        3: {"pikachu": "pikachu"},
    }
    encounters = encounter_by_area.get(area_number, {"empty_pokemon1": "empty_p_url1"})

    result = [{"name": name, "id": url} for name, url in encounters.items()]
    print(f"DEBUG: get_encounter_by_area({area_number}) -> {result}")
    return result

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
    generations = get_generations()
    return render_template('selection.html', generations=generations)


@app.route('/result')
def result():
    generation = request.args.get('generation')
    location = request.args.get('location')
    area = request.args.get('area')
    pokemon_name = request.args.get('pokemon_name')

    pokemon_data = get_pokemon_data(pokemon_name)

    return render_template(
        'result.html',
        generation=generation,
        location=location,
        area=area,
        pokemon_data=pokemon_data
    )


# --- API routes (return JSON, called by fetch() in the browser) -----------

@app.route('/api/locations')
def api_locations():
    generation = request.args.get('generation', type=int)
    if generation is None:
        return jsonify([])

    locations : list[dict[str, str]] = get_locations_for_generation(generation)
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

    encounters = get_encounter_by_area(area_number)
    return jsonify(encounters)



if __name__ == '__main__':
    app.run(debug=True)