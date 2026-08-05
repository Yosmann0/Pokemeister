import requests
import json
import re
from typing import List
from collections import defaultdict

URL_BASE = "https://pokeapi.co/api/v2/"

with open("files/game_list.json", "r") as file:
    list_data = json.load(file)

FULL_LIST = list_data["list"]

session = requests.Session()

def get_trailing_number(url:str) -> int:
    return int(re.search(r'(\d+)/?$', url).group(1))

def get_all_games() -> List[str]:
    return [game_list['name'] for game_list in FULL_LIST]

def get_generation_by_game(game_str:str):
    return next(region_list['generation'] for region_list in FULL_LIST if region_list['name'] == game_str)

def get_region_by_game(game_str:str) -> List[str]:
    return next(region_list['region'] for region_list in FULL_LIST if region_list['name'] == game_str)

def get_locations_by_region(region:str):
    response_gen = session.get(f"{URL_BASE}region/{region}/")
    
    data_gen = response_gen.json()

    data_locations = data_gen['locations']
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: get_trailing_number(item["url"]) for item in data_locations}
    list_locations = [{"name": name, "id": number} for name, number in list_locations.items()]
    
    return list_locations

def get_areas_by_location(location_num:int):
    response_loc = session.get(f"{URL_BASE}location/{location_num}/")

    data_loc = response_loc.json()

    data_area = data_loc['areas']
    list_area = [key for key in data_area]
    list_area = {item["name"]: get_trailing_number(item["url"]) for item in data_area}
    list_area = [{"name": name, "id": number} for name, number in list_area.items()]

    return list_area

def get_encounter_by_area(area_num:int):
    
    response_enc = session.get(f"{URL_BASE}location-area/{area_num}/")

    data_enc = response_enc.json()

    data_enc = data_enc['pokemon_encounters']
    list_enc = [key for key in data_enc]
    list_enc = [item['pokemon'] for item in list_enc]
    pokemon_list = {item["name"]: get_trailing_number(item["url"]) for item in list_enc}
    pokemon_list= [{"name": name, "id": number} for name, number in pokemon_list.items()]

    return pokemon_list

def get_encounter_by_area_filtered(area_num:int, game_str:str):
    
    response_enc = session.get(f"{URL_BASE}location-area/{area_num}/")

    data_enc = response_enc.json()

    data_enc = data_enc['pokemon_encounters']
    filtered_enc = [key for key in data_enc if any(version_detail['version']['name'] == game_str for version_detail in key['version_details'])]
    list_enc = [item['pokemon'] for item in filtered_enc]
    pokemon_list = {item["name"]: get_trailing_number(item["url"]) for item in list_enc}
    pokemon_list= [{"name": name, "id": number} for name, number in pokemon_list.items()]

    return pokemon_list

def get_encounter_by_area_filtered_methods(area_num:int, game_str:str, methods_list:list[str]):
    
    response_enc = session.get(f"{URL_BASE}location-area/{area_num}/")

    data_enc = response_enc.json()

    data_enc = data_enc['pokemon_encounters']
    filtered_enc = [key for key in data_enc if any(version_detail['version']['name'] == game_str and any(method['method']['name'] in methods_list for method in version_detail['encounter_details']) for version_detail in key['version_details'])]
    list_enc = [item['pokemon'] for item in filtered_enc]
    pokemon_list = {item["name"]: get_trailing_number(item["url"]) for item in list_enc}
    pokemon_list= [{"name": name, "id": number} for name, number in pokemon_list.items()]

    return pokemon_list

def get_encounter_info_by_pokemon(area_num: int, game_str: str, pokemon_str: str):
    response = session.get(f"{URL_BASE}location-area/{area_num}/")
    response.raise_for_status()

    encounters = response.json()["pokemon_encounters"]

    for encounter in encounters:
        if encounter["pokemon"]["name"] != pokemon_str:
            continue

        for version in encounter["version_details"]:
            if version["version"]["name"] != game_str:
                continue

            methods = defaultdict(list)

            
            for detail in version["encounter_details"]:
                methods[detail["method"]["name"]].append(detail)

            
            return [
                {
                    "method": method,
                    "chance": sum(d["chance"] for d in details),
                    "min_level": min(d["min_level"] for d in details),
                    "max_level": max(d["max_level"] for d in details)} for method, details in methods.items()]

    return []

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

def get_pokewiki_link(item_str:str):
    if '-' in item_str:
        item_str = item_str.replace('-', '_')

    if ' ' in item_str:
        item_str = item_str.replace(' ', '_')

    item_str = "_".join([part.capitalize() if i > 0 else part for i, part in enumerate(item_str.split("_"))])

    return(f"https://www.pokewiki.de/{item_str}")

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
    
    response = session.get(data['locations'][36]['url'])
    
    data = response.json()
    
    data_locations = data['areas']
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: get_trailing_number(item["url"]) for item in data_locations}
    list_locations = [{"name": name, "id": number} for name, number in list_locations.items()]
    print(list_locations)
    
    print(data['areas'][0]['name'], data['areas'][0]['url'])

    Edition = "leafgreen"
    
    
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
    print(FULL_LIST)
    kanto_list = [game['name'] for game in FULL_LIST if 'kanto' in game['region']]
    print(kanto_list)
    print(get_generation_by_game('heartgold'))
    print(get_region_by_game('heartgold'))
    print(get_all_games())

    list_locations = get_encounter_by_area_filtered(get_trailing_number(data['areas'][0]['url']), Edition)
    
    print(list_locations, f"Anzahl der Encounter für Edition {Edition}: {len(list_locations)}")

    print(get_encounter_by_area_filtered_methods(get_trailing_number(data['areas'][0]['url']), Edition, ['walk']))

    print(get_encounter_info_by_pokemon(get_trailing_number(data['areas'][0]['url']), Edition, 'magneton'))
    print(get_pokewiki_link('rock smash'))