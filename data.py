import requests
import json
import re
from typing import List
from collections import defaultdict
from enum import Enum
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

URL_BASE = "https://pokeapi.co/api/v2/"

with open("files/game_list.json", "r") as file:
    list_data = json.load(file)

FULL_LIST = list_data["list"]

GAMES = {
    # Generation 1
    'red': {'generation': 1, 'version-group': 1, 'version': 1},
    'blue': {'generation': 1, 'version-group': 1, 'version': 2},
    'yellow': {'generation': 1, 'version-group': 2, 'version': 3},

    # Generation 2
    'gold': {'generation': 2, 'version-group': 3, 'version': 4},
    'silver': {'generation': 2, 'version-group': 3, 'version': 5},
    'crystal': {'generation': 2, 'version-group': 4, 'version': 6},

    # Generation 3
    'ruby': {'generation': 3, 'version-group': 5, 'version': 7},
    'sapphire': {'generation': 3, 'version-group': 5, 'version': 8},
    'emerald': {'generation': 3, 'version-group': 6, 'version': 9},
    'firered': {'generation': 3, 'version-group': 7, 'version': 10},
    'leafgreen': {'generation': 3, 'version-group': 7, 'version': 11},
    'colosseum': {'generation': 3, 'version-group': 12, 'version': 19},
    'xd': {'generation': 3, 'version-group': 13, 'version': 20},

    # Generation 4
    'diamond': {'generation': 4, 'version-group': 8, 'version': 12},
    'pearl': {'generation': 4, 'version-group': 8, 'version': 13},
    'platinum': {'generation': 4, 'version-group': 9, 'version': 14},
    'heartgold': {'generation': 4, 'version-group': 10, 'version': 15},
    'soulsilver': {'generation': 4, 'version-group': 10, 'version': 16},

    # Generation 5
    'black': {'generation': 5, 'version-group': 11, 'version': 17},
    'white': {'generation': 5, 'version-group': 11, 'version': 18},
    'black2': {'generation': 5, 'version-group': 14, 'version': 21},
    'white2': {'generation': 5, 'version-group': 14, 'version': 22},

    # Generation 6
    'x': {'generation': 6, 'version-group': 15, 'version': 23},
    'y': {'generation': 6, 'version-group': 15, 'version': 24},
    'omegaruby': {'generation': 6, 'version-group': 16, 'version': 25},
    'alphasapphire': {'generation': 6, 'version-group': 16, 'version': 26},

    # Generation 7
    'sun': {'generation': 7, 'version-group': 17, 'version': 27},
    'moon': {'generation': 7, 'version-group': 17, 'version': 28},
    'ultrasun': {'generation': 7, 'version-group': 18, 'version': 29},
    'ultramoon': {'generation': 7, 'version-group': 18, 'version': 30},
    'letsgopikachu': {'generation': 7, 'version-group': 19, 'version': 31},
    'letsgoeevee': {'generation': 7, 'version-group': 19, 'version': 32},

    # Generation 8
    'sword': {'generation': 8, 'version-group': 20, 'version': 33},
    'shield': {'generation': 8, 'version-group': 20, 'version': 34},
    'the_isle_of_armor': {'generation': 8, 'version-group': 21, 'version': 35},  # DLC
    'the_crown_tundra': {'generation': 8, 'version-group': 22, 'version': 36},   # DLC
    'brilliantdiamond': {'generation': 8, 'version-group': 23, 'version': 37},
    'shiningpearl': {'generation': 8, 'version-group': 23, 'version': 38},
    'legends_arceus': {'generation': 8, 'version-group': 24, 'version': 39},

    # Generation 9
    'scarlet': {'generation': 9, 'version-group': 25, 'version': 40},
    'violet': {'generation': 9, 'version-group': 25, 'version': 41},
    'the_teal_mask': {'generation': 9, 'version-group': 26, 'version': 42},      # DLC
    'the_indigo_disk': {'generation': 9, 'version-group': 27, 'version': 43},    # DLC
}

class EncounterMethods(Enum):
    WALK = 'walk'
    OLD_ROD = 'old-rod'
    GOOD_ROD = 'good-rod'
    SUPER_ROD = 'super-rod'
    SURF = 'surf'
    ROCK_SMASH = 'rock-smash'
    HEADBUTT = 'headbutt'
    DARK_GRASS = 'dark-grass'
    GRASS_SPOTS = 'grass-spots'
    CAVE_SPOTS = 'cave-spots'
    BRIDGE_SPOTS = 'bridge-spots'
    SUPER_ROD_SPOTS = 'super-rod-spots'
    SURF_SPOTS = 'surf-spots'
    YELLOW_FLOWERS = 'yellow-flowers'
    PURPLE_FLOWERS = 'purple-flowers'
    RED_FLOWERS = 'red-flowers'
    ROUGH_TERRAIN = 'rough-terrain'
    GIFT = 'gift'
    GIFT_EGG = 'gift-egg'
    STATIC = 'static'
    POKEFLUTE = 'pokeflute'

session = requests.Session()

def get_trailing_number(url:str) -> int:
    return int(re.search(r'(\d+)/?$', url).group(1))

def get_all_games() -> List[str]:
    return [game_list['name'] for game_list in FULL_LIST]

def get_generation_by_game(game_str:str):
    return next(region_list['generation'] for region_list in FULL_LIST if region_list['name'] == game_str)

def get_region_by_game(game_str:str) -> List[str]:
    return next(region_list['region'] for region_list in FULL_LIST if region_list['name'] == game_str)

def get_version_group_by_version(game_str:str):
    response_ver = session.get(f"{URL_BASE}version/{game_str}/")
    data_ver = response_ver.json()
    return data_ver['version_group']['name']

def get_all_pokemon_by_gen(gen_num:int=None, filter_str:str=None) -> List[str]:
    pokemon_list = []
    for i in range(1, gen_num+1):
        data_gen = session.get(f"{URL_BASE}generation/{i}").json()
        for m in data_gen['pokemon_species']:
            pokemon_list.append(m['name'])
    return pokemon_list

@lru_cache(maxsize=None)
def get_version_group_id(group_str:str):
    data_group = session.get(f"{URL_BASE}version-group/{group_str}/").json()
    return data_group['id']

def get_group_id_by_game(game:str):
    return get_version_group_id(get_version_group_by_version(game))

def get_pokemon_sprite(name:str):
    data_pokemon = session.get(f"{URL_BASE}pokemon/{name}/").json()
    return data_pokemon['sprites']['front_default']

def get_pokemon_abilities(name: str, game_str: str):
    generation = get_generation_by_game(game_str)

    data = session.get(f"{URL_BASE}pokemon/{name}/").json()

    # current abilities, keyed by slot (1, 2 = normal, 3 = hidden)
    abilities = {
        a['slot']: {'name': a['ability']['name'], 'hidden': a['is_hidden']}
        for a in data['abilities']
    }

    applicable = [
        (get_trailing_number(p['generation']['url']), p)
        for p in data['past_abilities']
        if get_trailing_number(p['generation']['url']) >= generation
    ]

    # apply the furthest generation first so the closest one wins
    for _, past in sorted(applicable, key=lambda pair: pair[0], reverse=True):
        for a in past['abilities']:
            if a['ability'] is None:
                abilities.pop(a['slot'], None)  # slot didn't exist back then
            else:
                abilities[a['slot']] = {'name': a['ability']['name'], 'hidden': a['is_hidden']}

    return [
        {**ability, 'slot': slot, 'link': get_pokewiki_link(ability['name'])}
        for slot, ability in sorted(abilities.items())
    ]

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
                    "max_level": max(d["max_level"] for d in details)
                } for method, details in methods.items()
            ]

    return []

#this should be game_str instead of group_id for consistency
@lru_cache(maxsize=None)
def get_move_info(move_str: str, group_id: int):
    move_json = session.get(f"{URL_BASE}move/{move_str}/").json()

    move_dict = {
        'name': move_json['name'],
        'accuracy': move_json['accuracy'],
        'power': move_json['power'],
        'pp': move_json['pp'],
        'priority': move_json['priority'],
        'category': move_json['damage_class']['name'],
        'type': move_json['type']['name'],
    }

    applicable = [
        (get_version_group_id(p['version_group']['name']), p)
        for p in move_json['past_values']
        if group_id <= get_version_group_id(p['version_group']['name'])
    ]

    if applicable:
        _, past = min(applicable, key=lambda pair: pair[0])
        for field in ('accuracy', 'power', 'pp'):
            if past.get(field) is not None:
                move_dict[field] = past[field]
        if past.get('type') is not None:
            move_dict['type'] = past['type']['name']

    #pre gen 4 move categories
    category = move_dict['category']
    if group_id < 8: #uses group id because moves change between games not generations (group id 8 = diamond/pearl)
        if category != 'status':
            if category in ['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost', 'steel']:
                move_dict['category'] = 'physical'
            else:
                move_dict['category'] = 'special'

    return move_dict

def get_pokemon_info_by_name(area_num:int, game_str:str, pokemon_name:str):
    
    pokemon_url_data = session.get(f"{URL_BASE}pokemon/{pokemon_name}")
    pokemon_json_data = pokemon_url_data.json()
    version_group = get_version_group_by_version(game_str)
    version_group_id = get_version_group_id(version_group)
    
    pokemon_dict:dict = dict(name = f"{pokemon_json_data['name']}", stats = {"HP": pokemon_json_data['stats'][0]['base_stat'], "ATK": pokemon_json_data['stats'][1]['base_stat'], "DEF": pokemon_json_data['stats'][2]['base_stat'], "SPEATK": pokemon_json_data['stats'][3]['base_stat'], "SPEDEF": pokemon_json_data['stats'][4]['base_stat'], "SPE": pokemon_json_data['stats'][5]['base_stat']})
    pokemon_dict['id'] = pokemon_json_data['id']
    pokemon_dict['typing'] = {i['type']['name'] for i in pokemon_json_data['types']}
    pokemon_dict['species'] = f"{pokemon_json_data['species']['name']}"
    pokemon_dict["pokewiki_url"] = f"https://www.pokewiki.de/{pokemon_dict['species']}"
    pokemon_dict['stats']["BST"] = pokemon_dict['stats']['HP'] + pokemon_dict['stats']['ATK'] + pokemon_dict['stats']['DEF'] + pokemon_dict['stats']['SPEATK'] + pokemon_dict['stats']['SPEDEF'] + pokemon_dict['stats']['SPE']
    pokemon_dict['height'] = pokemon_json_data['height']
    pokemon_dict['weight'] = pokemon_json_data['weight']
    pokemon_dict['abilities'] = get_pokemon_abilities(pokemon_name, game_str)
    pokemon_dict['sprite'] = get_pokemon_sprite(pokemon_name)
    pokemon_dict['encounters'] = get_encounter_info_by_pokemon(area_num, game_str, pokemon_name)
    move_names = {
        m['move']['name']
        for m in pokemon_json_data['moves']
        if any(d['version_group']['name'] == version_group
            for d in m['version_group_details'])
    }

    with ThreadPoolExecutor(max_workers=10) as pool:
        list(pool.map(lambda name: get_move_info(name, version_group_id), move_names))
    
    pokemon_dict['moves'] = [
        {
            **get_move_info(key['move']['name'], version_group_id),
            'link': get_pokewiki_link(key['move']['name']),
            'method': version_group_detail['move_learn_method']['name'],
            **(
                {'learned_at': version_group_detail['level_learned_at']}
                if version_group_detail['move_learn_method']['name'] == 'level-up'
                else {}
                )
            

        } 
        for key in pokemon_json_data['moves']
        for version_group_detail in key['version_group_details']
        if version_group_detail['version_group']['name'] == version_group
        ]
    pokemon_dict['moves'].sort(key=lambda x: x['method'])
    return pokemon_dict

def get_less_pokemon_info_by_name(game_str:str, pokemon_name:str) -> dict:
    """
    returns pokemon data
    
    Args:
        game_str(str): String of Game
        pokemon_name(str): String of Pokemon

    Returns:
        name(str): Name of Pokemon
        stats(dict[int]): dict for Pokemon Basestats
        id(int): Dex number of Pokemon
        typing(List[str]): typing of Pokemon
        abilities(List[str]): List of the Pokemons abilities
        height(int): height of Pokemon
        weight(int): weight of Pokemon
        moves(List[str]): List of the Pokemons moves
    """
    
    pokemon_url_data = session.get(f"{URL_BASE}pokemon/{pokemon_name}")
    pokemon_json_data = pokemon_url_data.json()
    version_group = get_version_group_by_version(game_str)
    
    pokemon_dict:dict = dict(name = f"{pokemon_json_data['name']}", stats = {"HP": pokemon_json_data['stats'][0]['base_stat'], "ATK": pokemon_json_data['stats'][1]['base_stat'], "DEF": pokemon_json_data['stats'][2]['base_stat'], "SPEATK": pokemon_json_data['stats'][3]['base_stat'], "SPEDEF": pokemon_json_data['stats'][4]['base_stat'], "SPE": pokemon_json_data['stats'][5]['base_stat']})
    pokemon_dict['id'] = pokemon_json_data['id']
    pokemon_dict['typing'] = [i['type']['name'] for i in pokemon_json_data['types']]
    pokemon_dict['abilities'] = [i['name'] for i in get_pokemon_abilities(pokemon_name, game_str)]
    pokemon_dict['height'] = pokemon_json_data['height']
    pokemon_dict['weight'] = pokemon_json_data['weight']
    pokemon_dict['moves'] = [
        m['move']['name']
        for m in pokemon_json_data['moves']
        if any(d['version_group']['name'] == version_group
            for d in m['version_group_details'])
    ]
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

    print(get_pokemon_info_by_name(get_trailing_number(data['areas'][2]['url']), Edition, 'mewtwo'))
    print(get_pokewiki_link('brick-break'))
    print(get_version_group_by_version('x'))
    print(get_version_group_id(get_version_group_by_version('x')))
    print(get_move_info('thunder-wave', 1))
    print(get_move_info('thunder-wave', 25))
    print(get_less_pokemon_info_by_name('x', 'mewtwo'))
    print(get_less_pokemon_info_by_name('y', 'aegislash-shield'))
    a = get_all_pokemon_by_gen(GAMES['emerald']['generation'])
    print(a)
    print(get_move_info('fire-punch', GAMES['emerald']['version-group']))