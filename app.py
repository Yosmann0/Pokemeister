from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def get_generations():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]


def get_locations_for_generation(generation):
    # Pretend different generations have different locations available.
    locations_by_generation = {
        1: ["Kanto Route 1", "Viridian Forest", "Mt. Moon"],
        2: ["Johto Route 29", "Sprout Tower"],
        3: ["Hoenn Route 101", "Petalburg Woods"],
    }
    return locations_by_generation.get(generation, ["Unknown Location"])


def get_areas_for_location(location):
    areas_by_location = {
        "Kanto Route 1": ["Grass Patch", "Tall Grass"],
        "Viridian Forest": ["Entrance", "Deep Forest"],
        "Mt. Moon": ["Ground Floor", "B1F", "B2F"],
    }
    return areas_by_location.get(location, ["Area 1", "Area 2"])


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

    locations = get_locations_for_generation(generation)
    return jsonify(locations)


@app.route('/api/areas')
def api_areas():
    location = request.args.get('location')
    if not location:
        return jsonify([])

    areas = get_areas_for_location(location)
    return jsonify(areas)


if __name__ == '__main__':
    app.run(debug=True)