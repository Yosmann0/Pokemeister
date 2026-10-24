from math import floor, ceil
from enum import Enum
from data import (
    get_less_pokemon_info_by_name,
    get_move_info,
    get_group_id_by_game,
    GAMES
)

CHART_5 = {
    'normal':   {'rock': 0.5, 'steel': 0.5, 'ghost': 0},
    'fire':     {'fire': 0.5, 'water': 0.5, 'rock': 0.5, 'dragon': 0.5, 'grass': 2, 'ice': 2, 'bug': 2, 'steel': 2},
    'water':    {'water': 0.5, 'grass': 0.5, 'dragon': 0.5, 'fire': 2, 'ground': 2, 'rock': 2},
    'electric': {'electric': 0.5, 'grass': 0.5, 'dragon': 0.5, 'ground': 0, 'water': 2, 'flying': 2},
    'grass':    {'fire': 0.5, 'grass': 0.5, 'poison': 0.5, 'flying': 0.5, 'bug': 0.5, 'dragon': 0.5, 'steel': 0.5, 'water': 2, 'ground': 2, 'rock': 2},
    'ice':      {'fire': 0.5, 'water': 0.5, 'ice': 0.5, 'steel': 0.5, 'grass': 2, 'ground': 2, 'flying': 2, 'dragon': 2},
    'fighting': {'poison': 0.5, 'flying': 0.5, 'psychic': 0.5, 'bug': 0.5, 'ghost': 0, 'normal': 2, 'ice': 2, 'rock': 2, 'dark': 2, 'steel': 2},
    'poison':   {'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'ghost': 0.5, 'steel': 0, 'grass': 2},
    'ground':   {'grass': 0.5, 'bug': 0.5, 'flying': 0, 'fire': 2, 'electric': 2, 'poison': 2, 'rock': 2, 'steel': 2},
    'flying':   {'electric': 0.5, 'rock': 0.5, 'steel': 0.5, 'grass': 2, 'fighting': 2, 'bug': 2},
    'psychic':  {'psychic': 0.5, 'steel': 0.5, 'dark': 0, 'fighting': 2, 'poison': 2},
    'bug':      {'fire': 0.5, 'fighting': 0.5, 'poison': 0.5, 'flying': 0.5, 'ghost': 0.5, 'steel': 0.5, 'grass': 2, 'psychic': 2, 'dark': 2},
    'rock':     {'fighting': 0.5, 'ground': 0.5, 'steel': 0.5, 'fire': 2, 'ice': 2, 'flying': 2, 'bug': 2},
    'ghost':    {'normal': 0, 'dark': 0.5, 'steel': 0.5, 'psychic': 2, 'ghost': 2},
    'dragon':   {'steel': 0.5, 'dragon': 2},
    'dark':     {'fighting': 0.5, 'dark': 0.5, 'steel': 0.5, 'psychic': 2, 'ghost': 2},
    'steel':    {'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'steel': 0.5, 'ice': 2, 'rock': 2},
}

CHART_6 = {
    'normal':   {'rock': 0.5, 'steel': 0.5, 'ghost': 0},
    'fire':     {'fire': 0.5, 'water': 0.5, 'rock': 0.5, 'dragon': 0.5, 'grass': 2, 'ice': 2, 'bug': 2, 'steel': 2},
    'water':    {'water': 0.5, 'grass': 0.5, 'dragon': 0.5, 'fire': 2, 'ground': 2, 'rock': 2},
    'electric': {'electric': 0.5, 'grass': 0.5, 'dragon': 0.5, 'ground': 0, 'water': 2, 'flying': 2},
    'grass':    {'fire': 0.5, 'grass': 0.5, 'poison': 0.5, 'flying': 0.5, 'bug': 0.5, 'dragon': 0.5, 'steel': 0.5, 'water': 2, 'ground': 2, 'rock': 2},
    'ice':      {'fire': 0.5, 'water': 0.5, 'ice': 0.5, 'steel': 0.5, 'grass': 2, 'ground': 2, 'flying': 2, 'dragon': 2},
    'fighting': {'poison': 0.5, 'flying': 0.5, 'psychic': 0.5, 'fairy': 0.5, 'bug': 0.5, 'ghost': 0, 'normal': 2, 'ice': 2, 'rock': 2, 'dark': 2, 'steel': 2},
    'poison':   {'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'ghost': 0.5, 'steel': 0, 'grass': 2, 'fairy': 2},
    'ground':   {'grass': 0.5, 'bug': 0.5, 'flying': 0, 'fire': 2, 'electric': 2, 'poison': 2, 'rock': 2, 'steel': 2},
    'flying':   {'electric': 0.5, 'rock': 0.5, 'steel': 0.5, 'grass': 2, 'fighting': 2, 'bug': 2},
    'psychic':  {'psychic': 0.5, 'steel': 0.5, 'dark': 0, 'fighting': 2, 'poison': 2},
    'bug':      {'fire': 0.5, 'fighting': 0.5, 'poison': 0.5, 'flying': 0.5, 'fairy': 0.5, 'ghost': 0.5, 'steel': 0.5, 'grass': 2, 'psychic': 2, 'dark': 2},
    'rock':     {'fighting': 0.5, 'ground': 0.5, 'steel': 0.5, 'fire': 2, 'ice': 2, 'flying': 2, 'bug': 2},
    'ghost':    {'normal': 0, 'dark': 0.5, 'psychic': 2, 'ghost': 2},
    'dragon':   {'steel': 0.5, 'fairy': 0, 'dragon': 2},
    'dark':     {'fighting': 0.5, 'dark': 0.5, 'fairy': 0.5, 'psychic': 2, 'ghost': 2},
    'steel':    {'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'steel': 0.5, 'ice': 2, 'rock': 2, 'fairy': 2},
    'fairy':    {'fire': 0.5, 'poison': 0.5, 'steel': 0.5, 'fighting': 2, 'dragon': 2, 'dark': 2}
}

class Natures(Enum):
    HARDY =     [1, 1, 1, 1, 1]
    LONELY =    [1.1, 0.9, 1, 1, 1]
    ADAMANT =   [1.1, 1, 0.9, 1, 1]
    NAUGHTY =   [1.1, 1, 1, 0.9, 1]
    BRAVE =     [1.1, 1, 1, 1, 0.9]
    BOLD =      [0.9, 1.1, 1, 1, 1]
    DOCILE =    [1, 1, 1, 1, 1]
    IMPISH =    [1, 1.1, 0.9, 1, 1]
    LAX =       [1, 1.1, 1, 0.9, 1]
    RELAXED =   [1, 1.1, 1, 1, 0.9]
    MODEST =    [0.9, 1, 1.1, 1, 1]
    MILD =      [1, 0.9, 1.1, 1, 1]
    BASHFUL =   [1, 1, 1, 1, 1]
    RASH =      [1, 1, 1.1, 0.9, 1]
    QUIET =     [1, 1, 1.1, 1, 0.9]
    CALM =      [0.9, 1, 1, 1.1, 1]
    GENTLE =    [1, 0.9, 1, 1.1, 1]
    CAREFUL =   [1, 1, 0.9, 1.1, 1]
    QUIRKY =    [1, 1, 1, 1, 1]
    SASSY =     [1, 1, 1, 1.1, 0.9]
    TIMID =     [0.9, 1, 1, 1, 1.1]
    HASTY =     [1, 0.9, 1, 1, 1.1]
    JOLLY =     [1, 1, 0.9, 1, 1.1]
    NAIVE =     [1, 1, 1, 0.9, 1.1]
    SERIOUS =   [1, 1, 1, 1, 1]

class Pokemon():
    def __init__(self, name:str, dex:int=None, abilities:list=None, moves:list=None, types:list=None, basestats:list=None):
        self.dex = dex
        self.name = name
        self.abilities = abilities
        self.level = 50
        self.moves = moves
        self.types = types
        self.basestats = basestats
        self.ivs:list = [0, 0, 0, 0, 0, 0]
        self.evs:list = [0, 0, 0, 0, 0, 0]
        self.gender:str = 'Genderless'
        self.nature:list = Natures.HARDY.value
        self.item:str = 'none'
        self.status:str = 'none'
        self.stats:list = [1, 1, 1, 1, 1, 1]
        self.update_hp()
        self.update_stats()

    def __str__(self):
        return f"------------------------------\nName:\t\t{self.name}\nDex:\t\t{self.dex}\nLevel:\t\t{self.level}\nAbilities:\t{self.abilities}\nMoves:\t\t{self.moves}\nTyping:\t\t{self.types}\nStats:\t\t{self.stats}\nItem:\t\t{self.item}\n------------------------------"
    
    def update_hp(self):
        if self.basestats == None: return
        if self.name != "shedinja":
            self.stats[0] = floor((2 * self.basestats[0] + self.ivs[0]+ floor(self.evs[0] / 4)) * self.level / 100) + self.level + 10
        else:
            self.stats[0] = 1

    def update_stats(self):
        if self.basestats == None: return
        self.stats[1] = floor((floor((2 * self.basestats[1] + self.ivs[1] + floor(self.evs[1] / 4)) * self.level / 100) + 5) * self.nature[0]) #attack
        self.stats[2] = floor((floor((2 * self.basestats[2] + self.ivs[2] + floor(self.evs[2] / 4)) * self.level / 100) + 5) * self.nature[1]) #defense
        self.stats[3] = floor((floor((2 * self.basestats[3] + self.ivs[3] + floor(self.evs[3] / 4)) * self.level / 100) + 5) * self.nature[2]) #special attack
        self.stats[4] = floor((floor((2 * self.basestats[4] + self.ivs[4] + floor(self.evs[4] / 4)) * self.level / 100) + 5) * self.nature[3]) #special defense
        self.stats[5] = floor((floor((2 * self.basestats[5] + self.ivs[5] + floor(self.evs[5] / 4)) * self.level / 100) + 5) * self.nature[4]) #speed

    @classmethod
    def get_pokemon(cls, name, game):
        info = get_less_pokemon_info_by_name(game, name)
        stats = [j for j in info['stats'].values()]
        return cls(name, info['id'], info['abilities'], info['moves'], info['typing'], stats)

#dummy method just returns the hp of pokemon 2 minus the attack of pokemon 1
def dummy_fight(pokemon_1:Pokemon, pokemon_2:Pokemon):
    x = pokemon_2.stats[0] - pokemon_1.stats[1]
    if x < 1:
        return f"{pokemon_2.name} died"
    else:
        return f"HP left:{x}"

#not finished
def damage_gen3(attacker:Pokemon, defender:Pokemon, move_name:str, game:str, info:dict):
    move = get_move_info(move_name, get_group_id_by_game(game))
    if move['power'] == None: return 0
    if move['category'] == 'physical':
        damage_high:float = (((2 * attacker.level / 5 + 2) * move['power'] * attacker.stats[1] / defender.stats[2] / 50))
        damage_low:float = damage_high * 0.85
    else:
        damage_high:float = (((2 * attacker.level / 5 + 2) * move['power'] * attacker.stats[3] / defender.stats[4] / 50))
        damage_low:float = damage_high * 0.85

    return f"{ceil(damage_low / defender.stats[0] * 100)}% - {ceil(damage_high / defender.stats[0] * 100)}%"

def info_get(info:dict):
    damage_info:dict = {}
    if info['burn']:
        damage_info['burn'] = 0.5

def type_chart_gen5(att_type:str, def_type_1:str, def_type_2:str = None) -> float:
    row = CHART_5[att_type]
    multiplier = row.get(def_type_1, 1)
    if def_type_2 is not None:
        multiplier *= row.get(def_type_2, 1)
    return multiplier

def type_chart_gen6(att_type:str, def_type_1:str, def_type_2:str = None) -> float:
    row = CHART_6[att_type]
    multiplier = row.get(def_type_1, 1)
    if def_type_2 is not None:
        multiplier *= row.get(def_type_2, 1)
    return multiplier

if __name__ == '__main__':
    pokemon_1 = Pokemon("snorlax", 143, ["immunity", "thick-fat", "gluttony"], ["mega-punch"], ["normal"], [160, 110, 65, 65, 110, 30])
    print(pokemon_1.dex)
    print(pokemon_1.name)
    print(pokemon_1.abilities)
    print(pokemon_1.level)
    print(pokemon_1.moves)
    print(pokemon_1.types)
    print(pokemon_1.basestats)
    print(pokemon_1.ivs)
    print(pokemon_1.evs)
    print(pokemon_1.gender)
    print(pokemon_1.nature)
    print(pokemon_1.item)
    print(pokemon_1.status)
    print(pokemon_1.stats)
    pokemon_1.nature = Natures.ADAMANT.value
    pokemon_1.update_stats()
    print(pokemon_1.stats)
    print(Natures.HARDY.value)
    print(pokemon_1)
    pokemon_2 = Pokemon.get_pokemon("mewtwo", 'x')
    print(pokemon_2)
    pokemon_3 = Pokemon.get_pokemon('zorua', 'x')
    print(pokemon_3)
    print(dummy_fight(pokemon_2, pokemon_3))
    print(get_move_info(pokemon_2.moves[1], GAMES['emerald']['version-group']))
    print(damage_gen3(pokemon_2, pokemon_3, 'psychic', 'x'))
    print(type_chart_gen6('ghost', 'fairy', 'steel'))