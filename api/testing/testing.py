import requests
import json
import random
import re

URL_BASE = "https://pokeapi.co/api/v2/"

def get_trailing_number(url:str) -> int:
    return int(re.search(r'(\d+)/?$', url).group(1))

def get_locations_for_generation(generation:int):
    response_gen = requests.get(f"{URL_BASE}generation/{generation}/")
    
    data_gen = response_gen.json()
    
    response_gen = requests.get(data_gen['main_region']['url'])
    
    data_gen = response_gen.json()

    data_locations = data_gen['locations']
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: get_trailing_number(item["url"]) for item in data_locations}
    list_locations = [{"name": name, "id": number} for name, number in list_locations.items()]
    
    return list_locations

def get_areas_for_location(location_num:int):
    response_loc = requests.get(f"{URL_BASE}location/{location_num}/")

    data_loc = response_loc.json()

    data_area = data_loc['areas']
    list_area = [key for key in data_area]
    list_area = {item["name"]: get_trailing_number(item["url"]) for item in data_area}
    list_area = [{"name": name, "id": number} for name, number in list_area.items()]

    return list_area

def get_pokemon_for_area(area_num:int):
    
    response_enc = requests.get(f"{URL_BASE}location-area/{area_num}/")

    data_enc = response_enc.json()

    data_enc = data_enc['pokemon_encounters']
    list_enc = [key for key in data_enc]
    list_enc = [item['pokemon'] for item in list_enc]
    pokemon_list = {item["name"]: get_trailing_number(item["url"]) for item in list_enc}
    pokemon_list= [{"name": name, "id": number} for name, number in pokemon_list.items()]

    return pokemon_list

def get_pokemon_info_by_name(pokemon_name:str):
    
    pokemon_url_data = requests.get(f"{URL_BASE}pokemon/{pokemon_name}")
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

if __name__ == '__main__':
    generation = [1,2,3,4,5,6,7,8]
    
    url = f"{URL_BASE}generation/{generation[0]}/"
    
    response = requests.get(url)
    
    data = response.json()
    
    print(data['main_region']['name'], data['main_region']['url'])
    
    response = requests.get(data['main_region']['url'])
    
    data = response.json()
    
    data_locations = data['locations']
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: get_trailing_number(item["url"]) for item in data_locations}
    list_locations = [{"name": name, "id": number} for name, number in list_locations.items()]
    print(list_locations)
    
    print(data['locations'][34]['name'], data['locations'][34]['url'])
    
    response = requests.get(data['locations'][34]['url'])
    
    data = response.json()
    
    data_locations = data['areas']
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: get_trailing_number(item["url"]) for item in data_locations}
    list_locations = [{"name": name, "id": number} for name, number in list_locations.items()]
    print(list_locations)
    
    print(data['areas'][0]['name'], data['areas'][0]['url'])
    
    response = requests.get(data['areas'][0]['url'])
    
    data = response.json()
    
    data_locations = data['pokemon_encounters']
    list_locations = [key for key in data_locations]
    list_locations = [item['pokemon'] for item in list_locations]
    list_locations = {item["name"]: get_trailing_number(item["url"]) for item in list_locations}
    list_locations = [{"name": name, "id": number} for name, number in list_locations.items()]
    print(list_locations)
    
    test = data['pokemon_encounters'][random.randint(0, (len(list_locations) - 1))]['pokemon']        #list length is 1 higher than index
    print(test)
    
    pokemon_url_data = requests.get(f"{URL_BASE}pokemon/pikachu")
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