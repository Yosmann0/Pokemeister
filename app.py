from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def get_generations():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]


def get_locations_for_generation(generation):
    locations_by_generation = {
        1: {"location1": "l_url1", "location2": "l_url2", "location3": "l_url3"},
        2: {"location4": "l_url4", "location5": "l_url5"},
        3: {"location6": "l_url6", "location7": "l_url7"},
    }
    locations = locations_by_generation.get(generation, {"Unknown Location": "unknown_url"})

    result = [{"key": name, "value": url} for name, url in locations.items()]
    print(f"DEBUG: get_locations_for_generation({generation}) -> {result}")
    return result


def get_areas_for_location(location_url):
    areas_by_location = {
        "l_url1": {"area1": "a_url1", "area2": "a_url2", "area3": "a_url3"},
        "l_url2": {"area1": "a_url4", "area2": "a_url5"},
        "l_url3": {"area1": "a_url6", "area2": "a_url7"},
    }
    areas = areas_by_location.get(location_url, {"empty_area1": "empty_a_url1"})

    result = [{"key": name, "value": url} for name, url in areas.items()]
    print(f"DEBUG: get_areas_for_location({location_url}) -> {result}")
    return result


def get_encounter_by_area(area_url):
    encounter_by_area = {
        "a_url1": {"pokemon1": "p_url1", "pokemon2": "p_url2", "pokemon3": "p_url3"},
        "a_url2": {"pokemon1": "p_url4", "pokemon2": "p_url5"},
        "a_url3": {"pokemon1": "p_url6", "pokemon2": "p_url7"},
    }
    encounters = encounter_by_area.get(area_url, {"empty_pokemon1": "empty_p_url1"})

    result = [{"key": name, "value": url} for name, url in encounters.items()]
    print(f"DEBUG: get_encounter_by_area({area_url}) -> {result}")
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
    return render_template('result.html', generation=generation, location=location, area=area)


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
    location = request.args.get('location')
    if not location:
        return jsonify([])

    areas = get_areas_for_location(location)
    return jsonify(areas)

@app.route('/api/encounters')
def api_encounters():
    area = request.args.get('area')
    if not area:
        return jsonify([])

    encounters = get_encounter_by_area(area)
    return jsonify(encounters)



if __name__ == '__main__':
    app.run(debug=True)