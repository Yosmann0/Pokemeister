from math import floor
from enum import Enum
from data import (
    get_less_pokemon_info_by_name,
)
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

#first number is the generation, second is version-group (import for move and ability list)
class Games(Enum):
    RUBY_SAPHIRE = [3, 5]
    EMERALD = [3, 6]
    FIRERED_LEAFGREEN = [3, 7]
    DIAMOND_PEARL = [4, 8]
    PLATINUM = [4, 9]
    HEARTGOLD_SOULSILVER = [4, 10]
    BLACK_WHITE = [5, 11]
    BLACK_WHITE2 = [5, 14]
    X_Y = [6, 15]
    OMEGARUBY_ALPHASAPPHIRE = [6, 16]
    SUN_MOON = [7, 17]
    ULTRASUN_ULTRAMOON = [7, 18]
    LETSGOPIKACHU_LETSGOEEVEE = [7, 19]
    SWORD_SHIELD = [8, 20]
    BRILLIANTDIAMOND_SHININGPEARL = [8, 23]


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




Pokemon_1 = Pokemon("snorlax", 143, ["immunity", "thick-fat", "gluttony"], ["mega-punch"], ["normal"], [160, 110, 65, 65, 110, 30])
print(Pokemon_1.dex)
print(Pokemon_1.name)
print(Pokemon_1.abilities)
print(Pokemon_1.level)
print(Pokemon_1.moves)
print(Pokemon_1.types)
print(Pokemon_1.basestats)
print(Pokemon_1.ivs)
print(Pokemon_1.evs)
print(Pokemon_1.gender)
print(Pokemon_1.nature)
print(Pokemon_1.item)
print(Pokemon_1.status)
print(Pokemon_1.stats)
Pokemon_1.nature = Natures.ADAMANT.value
Pokemon_1.update_stats()
print(Pokemon_1.stats)
print(Natures.HARDY.value)
print(Pokemon_1)
pokemon_2 = Pokemon.get_pokemon("mewtwo", 'x')
print(pokemon_2)
pokemon_3 = Pokemon.get_pokemon('zorua', 'omega-ruby')
print(pokemon_3)
print(dummy_fight(pokemon_2, pokemon_3))
