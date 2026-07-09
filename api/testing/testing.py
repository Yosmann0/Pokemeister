import requests
import pandas as pd
import json
import random

generation = [1,2,3,4,5,6,7,8,9]

url = f"https://pokeapi.co/api/v2/generation/{generation[0]}/"

response = requests.get(url)

data = response.json()

print(data['main_region']['url'])
print(data['main_region']['name'])

response = requests.get(data['main_region']['url'])

data = response.json()

data_locations = json.dumps(data['locations'])
data_locations = json.loads(data_locations)
list_locations = [key for key in data_locations]
list_locations = {item["name"]: item["url"] for item in data_locations}
print(list_locations)

print(data['locations'][30]['url'])
print(data['locations'][30]['name'])

response = requests.get(data['locations'][30]['url'])

data = response.json()

data_locations = json.dumps(data['areas'])
data_locations = json.loads(data_locations)
list_locations = [key for key in data_locations]
list_locations = {item["name"]: item["url"] for item in data_locations}
print(list_locations)

print(data['areas'][0]['url'])
print(data['areas'][0]['name'])

response = requests.get(data['areas'][0]['url'])

data = response.json()

data_locations = json.dumps(data['pokemon_encounters'])
data_locations = json.loads(data_locations)
list_locations = [key for key in data_locations]
list_locations = [item['pokemon'] for item in list_locations]
list_locations = {item["name"]: item["url"] for item in list_locations}
print(list_locations)


print(data['pokemon_encounters'][random.randint(0, len(list_locations))]['pokemon']['name'])


def get_locations_for_generation(generation:int):
    url = f"https://pokeapi.co/api/v2/generation/{generation}/"

    response = requests.get(url)

    data = response.json()

    print(data['main_region']['url'])
    print(data['main_region']['name'])

    response = requests.get(data['main_region']['url'])

    data = response.json()

    data_locations = json.dumps(data['locations'])
    data_locations = json.loads(data_locations)
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: item["url"] for item in data_locations}
    return list_locations

def get_areas_for_location(location_url:str):
    response = requests.get(location_url)

    data = response.json()

    data_locations = json.dumps(data['areas'])
    data_locations = json.loads(data_locations)
    list_locations = [key for key in data_locations]
    list_locations = {item["name"]: item["url"] for item in data_locations}
    print(list_locations)

def get_pokemon_info_by_url(pokemon_url:str):
    return("to be continued")