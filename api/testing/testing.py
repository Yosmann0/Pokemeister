import requests
import json
import random
import re
from concurrent.futures import ThreadPoolExecutor

URL_BASE = "https://pokeapi.co/api/v2/"

session = requests.Session()

def get_trailing_number(url:str) -> int:
    return int(re.search(r'(\d+)/?$', url).group(1))

def get_locations_for_generation(generation:int):
    response_gen = session.get(f"{URL_BASE}generation/{generation}/")
    
    data_gen = response_gen.json()
    
    response_gen = session.get(data_gen['main_region']['url'])
    
    data_gen = response_gen.json()

    data_locations = data_gen['locations']
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: get_trailing_number(item["url"]) for item in data_locations}
    list_locations = [{"name": name, "id": number} for name, number in list_locations.items()]
    
    return list_locations

def get_areas_for_location(location_num:int):
    response_loc = session.get(f"{URL_BASE}location/{location_num}/")

    data_loc = response_loc.json()

    data_area = data_loc['areas']
    list_area = [key for key in data_area]
    list_area = {item["name"]: get_trailing_number(item["url"]) for item in data_area}
    list_area = [{"name": name, "id": number} for name, number in list_area.items()]

    return list_area

def get_encounter_for_area(area_num:int):
    
    response_enc = session.get(f"{URL_BASE}location-area/{area_num}/")

    data_enc = response_enc.json()

    data_enc = data_enc['pokemon_encounters']
    list_enc = [key for key in data_enc]
    list_enc = [item['pokemon'] for item in list_enc]
    pokemon_list = {item["name"]: get_trailing_number(item["url"]) for item in list_enc}
    pokemon_list= [{"name": name, "id": number} for name, number in pokemon_list.items()]

    return pokemon_list

def get_encounter_for_area_filtered(area_num:int, game_str:str):
    
    response_enc = session.get(f"{URL_BASE}location-area/{area_num}/")

    data_enc = response_enc.json()

    data_enc = data_enc['pokemon_encounters']
    filtered_enc = [key for key in data_enc if any(version_detail['version']['name'] == game_str for version_detail in key['version_details'])]
    list_enc = [item['pokemon'] for item in filtered_enc]
    pokemon_list = {item["name"]: get_trailing_number(item["url"]) for item in list_enc}
    pokemon_list= [{"name": name, "id": number} for name, number in pokemon_list.items()]

    return pokemon_list

def get_pokemon_info_by_name(pokemon_name:str):
    
    pokemon_url_data = session.get(f"{URL_BASE}pokemon/{pokemon_name}")
    pokemon_json_data = pokemon_url_data.json()
    
    pokemon_dict:dict = dict(name = f"{pokemon_json_data['name']}", stats = {"HP": pokemon_json_data['stats'][0]['base_stat'], "ATK": pokemon_json_data['stats'][1]['base_stat'], "DEF": pokemon_json_data['stats'][2]['base_stat'], "SPEATK": pokemon_json_data['stats'][3]['base_stat'], "SPEDEF": pokemon_json_data['stats'][4]['base_stat'], "SPE": pokemon_json_data['stats'][5]['base_stat']})
    pokemon_dict['id'] = pokemon_json_data['id']
    pokemon_dict['typing'] = {i['type']['name'] for i in pokemon_json_data['types']}
    pokemon_dict['species'] = f"{pokemon_json_data['species']['name']}"
    pokemon_dict["pokewiki_url"] = f"https://www.pokewiki.de/{pokemon_dict['species']}"
    pokemon_dict['stats']["BST"] = pokemon_dict['stats']['HP'] + pokemon_dict['stats']['ATK'] + pokemon_dict['stats']['DEF'] + pokemon_dict['stats']['SPEATK'] + pokemon_dict['stats']['SPEDEF'] + pokemon_dict['stats']['SPE']
    pokemon_dict['height'] = pokemon_json_data['height']
    pokemon_dict['weight'] = pokemon_json_data['weight']
    pokemon_dict['sprite'] = f"{pokemon_json_data['sprites']['front_default']}"

    return pokemon_dict

def fetch_by_id(endpoint, i):
    response_id = session.get(f"{URL_BASE}{endpoint}/{i}/")
    response_id.raise_for_status()
    data_id = response_id.json()
    return {'name': data_id['name'], 'id': data_id['id']}

def get_full_list(endpoint, id_range, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(lambda i: fetch_by_id(endpoint, i), id_range))

def get_full_version_list():
    return get_full_list('version', range(1, 40))

def get_full_version_group_list():
    return get_full_list('version-group', range(1, 25))

def get_full_region_list():
    return get_full_list('region', range(1, 10))

def get_full_generation_list():
    return get_full_list('generation', range(1, 9))

def get_final_version_list():
    return [
    {'name': 'red', 'id': 1, 'generation': 1, 'region': ['kanto']},
    {'name': 'blue', 'id': 2, 'generation': 1, 'region': ['kanto']},
    {'name': 'yellow', 'id': 3, 'generation': 1, 'region': ['kanto']},
    {'name': 'gold', 'id': 4, 'generation': 2, 'region': ['johto', 'kanto']},
    {'name': 'silver', 'id': 5, 'generation': 2, 'region': ['johto', 'kanto']},
    {'name': 'crystal', 'id': 6, 'generation': 2, 'region': ['johto', 'kanto']},
    {'name': 'ruby', 'id': 7, 'generation': 3, 'region': ['hoenn']},
    {'name': 'sapphire', 'id': 8, 'generation': 3, 'region': ['hoenn']},
    {'name': 'emerald', 'id': 9, 'generation': 3, 'region': ['hoenn']},
    {'name': 'firered', 'id': 10, 'generation': 3, 'region': ['kanto']},
    {'name': 'leafgreen', 'id': 11, 'generation': 3, 'region': ['kanto']},
    {'name': 'diamond', 'id': 12, 'generation': 4, 'region': ['sinnoh']},
    {'name': 'pearl', 'id': 13, 'generation': 4, 'region': ['sinnoh']},
    {'name': 'platinum', 'id': 14, 'generation': 4, 'region': ['sinnoh']},
    {'name': 'heartgold', 'id': 15, 'generation': 4, 'region': ['johto', 'kanto']},
    {'name': 'soulsilver', 'id': 16, 'generation': 4, 'region': ['johto', 'kanto']},
    {'name': 'black', 'id': 17, 'generation': 5, 'region': ['unova']},
    {'name': 'white', 'id': 18, 'generation': 5, 'region': ['unova']},
    {'name': 'black-2', 'id': 19, 'generation': 5, 'region': ['unova']},
    {'name': 'white-2', 'id': 20, 'generation': 5, 'region': ['unova']},
    {'name': 'x', 'id': 21, 'generation': 6, 'region': ['kalos']},
    {'name': 'y', 'id': 22, 'generation': 6, 'region': ['kalos']},
    {'name': 'omega-ruby', 'id': 23, 'generation': 6, 'region': ['hoenn']},
    {'name': 'alpha-sapphire', 'id': 24, 'generation': 6, 'region': ['hoenn']},
    {'name': 'sun', 'id': 25, 'generation': 7, 'region': ['alola']},
    {'name': 'moon', 'id': 26, 'generation': 7, 'region': ['alola']},
    {'name': 'ultra-sun', 'id': 27, 'generation': 7, 'region': ['alola']},
    {'name': 'ultra-moon', 'id': 28, 'generation': 7, 'region': ['alola']},
    {'name': 'lets-go-pikachu', 'id': 29, 'generation': 7, 'region': ['kanto']},
    {'name': 'lets-go-eevee', 'id': 30, 'generation': 7, 'region': ['kanto']},
    {'name': 'sword', 'id': 31, 'generation': 8, 'region': ['galar']},
    {'name': 'shield', 'id': 32, 'generation': 8, 'region': ['galar']},
    {'name': 'brilliant-diamond', 'id': 33, 'generation': 8, 'region': ['sinnoh']},
    {'name': 'shining-pearl', 'id': 34, 'generation': 8, 'region': ['sinnoh']},
    {'name': 'legends-arceus', 'id': 35, 'generation': 8, 'region': ['hisui']}]

if __name__ == '__main__':
    generation = [1,2,3,4,5,6,7,8]
    
    url = f"{URL_BASE}generation/{generation[0]}/"
    
    response = session.get(url)
    
    data = response.json()
    
    print(data['main_region']['name'], data['main_region']['url'])
    
    response = session.get(data['main_region']['url'])
    
    data = response.json()
    
    data_locations = data['locations']
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: get_trailing_number(item["url"]) for item in data_locations}
    list_locations = [{"name": name, "id": number} for name, number in list_locations.items()]
    print(list_locations)
    
    print(data['locations'][34]['name'], data['locations'][34]['url'])
    
    response = session.get(data['locations'][34]['url'])
    
    data = response.json()
    
    data_locations = data['areas']
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: get_trailing_number(item["url"]) for item in data_locations}
    list_locations = [{"name": name, "id": number} for name, number in list_locations.items()]
    print(list_locations)
    
    print(data['areas'][0]['name'], data['areas'][0]['url'])

    Edition = "firered"
    list_locations = get_encounter_for_area_filtered(get_trailing_number(data['areas'][0]['url']), Edition)
    
    #response = session.get(data['areas'][0]['url'])
    #
    #data = response.json()
    #
    #data_locations = data['pokemon_encounters']
    #list_locations = [key for key in data_locations]
    #list_locations = [item['pokemon'] for item in list_locations]
    #list_locations = {item["name"]: get_trailing_number(item["url"]) for item in list_locations}
    #list_locations = [{"name": name, "id": number} for name, number in list_locations.items()]
    print(list_locations, f"Anzahl der Encounter für Edition {Edition}: {len(list_locations)}")
    
    pokemon_url_data = session.get(f"{URL_BASE}pokemon/pikachu")
    pokemon_json_data = pokemon_url_data.json()
    
    pokemon_dict:dict = dict(name = f"{pokemon_json_data['name']}", stats = {"HP": pokemon_json_data['stats'][0]['base_stat'], "ATK": pokemon_json_data['stats'][1]['base_stat'], "DEF": pokemon_json_data['stats'][2]['base_stat'], "SPEATK": pokemon_json_data['stats'][3]['base_stat'], "SPEDEF": pokemon_json_data['stats'][4]['base_stat'], "SPE": pokemon_json_data['stats'][5]['base_stat']})
    pokemon_dict['id'] = pokemon_json_data['id']
    pokemon_dict['typing'] = {i['type']['name'] for i in pokemon_json_data['types']}
    pokemon_dict['species'] = f"{pokemon_json_data['species']['name']}"
    pokemon_dict["pokewiki_url"] = f"https://www.pokewiki.de/{pokemon_dict['species']}"
    pokemon_dict['stats']["BST"] = pokemon_dict['stats']['HP'] + pokemon_dict['stats']['ATK'] + pokemon_dict['stats']['DEF'] + pokemon_dict['stats']['SPEATK'] + pokemon_dict['stats']['SPEDEF'] + pokemon_dict['stats']['SPE']
    pokemon_dict['height'] = pokemon_json_data['height']
    pokemon_dict['weight'] = pokemon_json_data['weight']
    pokemon_dict['sprite'] = f"{pokemon_json_data['sprites']['front_default']}"
    
    print(pokemon_dict, len(pokemon_dict))
    #version_groups = get_full_version_group_list()
    #print(version_groups)
    #version_list = get_full_version_list()
    #print(version_list)
    #region_list = get_full_region_list()
    #print(region_list)
    #generation_list = get_full_generation_list()
    #print(generation_list)
    final_list = get_final_version_list()
    print(final_list)
    kanto_list = [game['name'] for game in final_list if 'kanto' in game['region']]
    print(kanto_list)