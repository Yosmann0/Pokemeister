import requests
import json
import random

generation = [1,2,3,4,5,6,7,8]

url = f"https://pokeapi.co/api/v2/generation/{generation[0]}/"

response = requests.get(url)

data = response.json()

print(data['main_region']['name'], data['main_region']['url'])

response = requests.get(data['main_region']['url'])

data = response.json()

data_locations = data['locations']
list_locations = [key for key in data_locations]
list_locations = {item["name"]: item["url"] for item in data_locations}
#print(list_locations)

print(data['locations'][34]['name'], data['locations'][34]['url'])

response = requests.get(data['locations'][34]['url'])

data = response.json()

data_locations = data['areas']
list_locations = [key for key in data_locations]
list_locations = {item["name"]: item["url"] for item in data_locations}
#print(list_locations)

print(data['areas'][0]['name'], data['areas'][0]['url'])

response = requests.get(data['areas'][0]['url'])

data = response.json()

data_locations = data['pokemon_encounters']
list_locations = [key for key in data_locations]
list_locations = [item['pokemon'] for item in list_locations]
list_locations = {item["name"]: item["url"] for item in list_locations}
#print(list_locations)

test = data['pokemon_encounters'][random.randint(0, (len(list_locations) - 1))]['pokemon']        #list length is 1 higher than index
print(test)

pokemon_url_data = requests.get(test['url'])
pokemon_json_data = pokemon_url_data.json()
pokemon_dict:dict = dict(name = f"{pokemon_json_data['name']}", stats = {"HP": pokemon_json_data['stats'][0]['base_stat'], "ATK": pokemon_json_data['stats'][1]['base_stat'], "DEF": pokemon_json_data['stats'][2]['base_stat'], "SPEATK": pokemon_json_data['stats'][3]['base_stat'], "SPEDEF": pokemon_json_data['stats'][4]['base_stat'], "SPE": pokemon_json_data['stats'][5]['base_stat']})

pokemon_dict["pokewiki_url"] = f"https://www.pokewiki.de/{pokemon_dict['name']}"
pokemon_dict['stats']["BST"] = pokemon_dict['stats']['HP'] + pokemon_dict['stats']['ATK'] + pokemon_dict['stats']['DEF'] + pokemon_dict['stats']['SPEATK'] + pokemon_dict['stats']['SPEDEF'] + pokemon_dict['stats']['SPE']
pokemon_dict['typing'] = {i['type']['name'] for i in pokemon_json_data['types']}

print(pokemon_dict, len(pokemon_dict))

def get_locations_for_generation(generation:int):
    url = f"https://pokeapi.co/api/v2/generation/{generation}/"

    response = requests.get(url)
    
    data = response.json()
    
    response = requests.get(data['main_region']['url'])
    
    data = response.json()

    data_locations = data['locations']
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: item["url"] for item in data_locations}
    
    return list_locations

def get_areas_for_location(location_url:str):
    response = requests.get(location_url)

    data = response.json()

    data_locations = data['areas']
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: item["url"] for item in data_locations}
    return list_locations

def get_pokemon_for_area(area_url:str):
    
    response = requests.get(area_url)

    data = response.json()

    data_locations = data['pokemon_encounters']
    list_locations = [key for key in data_locations]
    list_locations = [item['pokemon'] for item in list_locations]
    pokemon_list = {item["name"]: item["url"] for item in list_locations}
    
    return pokemon_list

def get_pokemon_info_by_url(pokemon_name_url:dict):
    
    pokemon_url_data = requests.get(pokemon_name_url['url'])
    pokemon_json_data = pokemon_url_data.json()
    
    pokemon_dict:dict = dict(name = f"{pokemon_json_data['name']}", stats = {"HP": pokemon_json_data['stats'][0]['base_stat'], "ATK": pokemon_json_data['stats'][1]['base_stat'], "DEF": pokemon_json_data['stats'][2]['base_stat'], "SPEATK": pokemon_json_data['stats'][3]['base_stat'], "SPEDEF": pokemon_json_data['stats'][4]['base_stat'], "SPE": pokemon_json_data['stats'][5]['base_stat']})
    pokemon_dict['typing'] = {i['type']['name'] for i in pokemon_json_data['types']}
    pokemon_dict["pokewiki_url"] = f"https://www.pokewiki.de/{pokemon_dict['name']}"
    pokemon_dict['stats']["BST"] = pokemon_dict['stats']['HP'] + pokemon_dict['stats']['ATK'] + pokemon_dict['stats']['DEF'] + pokemon_dict['stats']['SPEATK'] + pokemon_dict['stats']['SPEDEF'] + pokemon_dict['stats']['SPE']
    
    return pokemon_dict