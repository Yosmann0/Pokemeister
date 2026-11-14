import json
from math import floor, ceil
from enum import Enum
from .data import (
    get_less_pokemon_info_by_name,
    get_move_info,
    get_group_id_by_game,
)


class Natures(Enum):
    HARDY = [1, 1, 1, 1, 1]
    LONELY = [1.1, 0.9, 1, 1, 1]
    ADAMANT = [1.1, 1, 0.9, 1, 1]
    NAUGHTY = [1.1, 1, 1, 0.9, 1]
    BRAVE = [1.1, 1, 1, 1, 0.9]
    BOLD = [0.9, 1.1, 1, 1, 1]
    DOCILE = [1, 1, 1, 1, 1]
    IMPISH = [1, 1.1, 0.9, 1, 1]
    LAX = [1, 1.1, 1, 0.9, 1]
    RELAXED = [1, 1.1, 1, 1, 0.9]
    MODEST = [0.9, 1, 1.1, 1, 1]
    MILD = [1, 0.9, 1.1, 1, 1]
    BASHFUL = [1, 1, 1, 1, 1]
    RASH = [1, 1, 1.1, 0.9, 1]
    QUIET = [1, 1, 1.1, 1, 0.9]
    CALM = [0.9, 1, 1, 1.1, 1]
    GENTLE = [1, 0.9, 1, 1.1, 1]
    CAREFUL = [1, 1, 0.9, 1.1, 1]
    QUIRKY = [1, 1, 1, 1, 1]
    SASSY = [1, 1, 1, 1.1, 0.9]
    TIMID = [0.9, 1, 1, 1, 1.1]
    HASTY = [1, 0.9, 1, 1, 1.1]
    JOLLY = [1, 1, 0.9, 1, 1.1]
    NAIVE = [1, 1, 1, 0.9, 1.1]
    SERIOUS = [1, 1, 1, 1, 1]


class Pokemon:
    def __init__(
        self,
        name: str,
        dex: int = None,
        abilities: list = None,
        moves: list = None,
        types: list = None,
        basestats: list = None,
    ):
        self.dex = dex
        self.name = name
        self.abilities = abilities
        self.level = 50
        self.moves = moves
        self.types = types
        self.basestats = basestats
        self.ivs: list = [0, 0, 0, 0, 0, 0]
        self.evs: list = [0, 0, 0, 0, 0, 0]
        self.gender: str = "Genderless"
        self.nature: list = Natures.HARDY.value
        self.item: str = "none"
        self.status: str = "none"
        self.stats: list = [1, 1, 1, 1, 1, 1]
        self.update()

    def __str__(self):
        return f"------------------------------\nName:\t\t{self.name}\nDex:\t\t{self.dex}\nLevel:\t\t{self.level}\nAbilities:\t{self.abilities}\nMoves:\t\t{self.moves}\nTyping:\t\t{self.types}\nStats:\t\t{self.stats}\nItem:\t\t{self.item}\n------------------------------"

    def update(self, changes: dict = {}):
        for x, y in changes.items():
            match (x):
                case "level":
                    self.level = y
                case "ivs":
                    self.ivs = y
                case "evs":
                    self.evs = y
                case "gender":
                    self.gender = y
                case "nature":
                    self.nature = y
                case "item":
                    self.item = y
                case "status":
                    self.status = y
        if self.basestats == None:
            return
        if self.name != "shedinja":
            self.stats[0] = (
                floor(
                    (2 * self.basestats[0] + self.ivs[0] + floor(self.evs[0] / 4))
                    * self.level
                    / 100
                )
                + self.level
                + 10
            )  # HP
        else:
            self.stats[0] = 1
        self.stats[1] = floor(
            (
                floor(
                    (2 * self.basestats[1] + self.ivs[1] + floor(self.evs[1] / 4))
                    * self.level
                    / 100
                )
                + 5
            )
            * self.nature[0]
        )  # attack
        self.stats[2] = floor(
            (
                floor(
                    (2 * self.basestats[2] + self.ivs[2] + floor(self.evs[2] / 4))
                    * self.level
                    / 100
                )
                + 5
            )
            * self.nature[1]
        )  # defense
        self.stats[3] = floor(
            (
                floor(
                    (2 * self.basestats[3] + self.ivs[3] + floor(self.evs[3] / 4))
                    * self.level
                    / 100
                )
                + 5
            )
            * self.nature[2]
        )  # special attack
        self.stats[4] = floor(
            (
                floor(
                    (2 * self.basestats[4] + self.ivs[4] + floor(self.evs[4] / 4))
                    * self.level
                    / 100
                )
                + 5
            )
            * self.nature[3]
        )  # special defense
        self.stats[5] = floor(
            (
                floor(
                    (2 * self.basestats[5] + self.ivs[5] + floor(self.evs[5] / 4))
                    * self.level
                    / 100
                )
                + 5
            )
            * self.nature[4]
        )  # speed

    @classmethod
    def get_pokemon(cls, name, game):
        info = get_less_pokemon_info_by_name(game, name)
        stats = [j for j in info["stats"].values()]
        return cls(
            name, info["id"], info["abilities"], info["moves"], info["typing"], stats
        )


# dummy method just returns the hp of pokemon 2 minus the attack of pokemon 1
def dummy_fight(pokemon_1: Pokemon, pokemon_2: Pokemon):
    x = pokemon_2.stats[0] - pokemon_1.stats[1]
    if x < 1:
        return f"{pokemon_2.name} died"
    else:
        return f"HP left:{x}"


def damage_gen3(
    attacker: Pokemon, defender: Pokemon, move_name: str, game: str, info: dict = {}
):
    """
    Returns the damage range.

    Args:
        attacker (Pokemon): The attacking Pokemon.
        defender (Pokemon): The defending Pokemon.
        move_name (str): Name of the move used.
        game (str): Name of the game.
        info (dict): Battle modifiers. Supported keys:
            burn (bool): Attacker is burned.
            reflect (bool): Reflect is active.
            light (bool): Light Screen is active.
            double (bool): Double battle.
            flashfire (bool): Flash Fire ability is active.
            weather (str): Which weather is active.
            stockpile (int): Number of Stockpile stacks.
            crit (bool): Attack is a critical hit.
            doubledamage (bool): Double damage is active.
            charge (bool): Charge is active.
            helpinghand (bool): Helping Hand is active.
            enemies (int): Number of enemies.
            allies (int): Number of allies.
    Returns:
        str: range of the attack damage in percent
    """
    move = get_move_info(move_name, get_group_id_by_game(game))
    if move["power"] == None:
        return 0
    if "double" not in info.keys():
        info["double"] = False
    if info["double"]:
        if move["category"] == "physical":
            state_info = get_info_gen_3_doubles(attacker, info, move)
            damage_high: float = (
                (
                    (
                        (2 * attacker.level / 5 + 2)
                        * move["power"]
                        * attacker.stats[1]
                        / defender.stats[2]
                        / 50
                    )
                    * state_info["burn"]
                    * state_info["reflect"]
                    * state_info["targets"]
                    * state_info["weather"]
                    * state_info["flashfire"]
                    + 2
                )
                * state_info["stockpile"]
                * state_info["crit"]
                * state_info["doubledamage"]
                * state_info["charge"]
                * state_info["helpinghand"]
                * state_info["stab"]
                * type_chart_gen5(move["type"], defender.types)
            )
            damage_low: float = damage_high * 0.85
        else:
            state_info = get_info_gen_3_doubles(attacker, info, move)
            damage_high: float = (
                (
                    (
                        (2 * attacker.level / 5 + 2)
                        * move["power"]
                        * attacker.stats[3]
                        / defender.stats[4]
                        / 50
                    )
                    * state_info["burn"]
                    * state_info["light"]
                    * state_info["targets"]
                    * state_info["weather"]
                    * state_info["flashfire"]
                    + 2
                )
                * state_info["stockpile"]
                * state_info["crit"]
                * state_info["doubledamage"]
                * state_info["charge"]
                * state_info["helpinghand"]
                * state_info["stab"]
                * type_chart_gen5(move["type"], defender.types)
            )
            damage_low: float = damage_high * 0.85
    else:
        if move["category"] == "physical":
            state_info = get_info_gen_3(attacker, info, move)
            damage_high: float = (
                (
                    (
                        (2 * attacker.level / 5 + 2)
                        * move["power"]
                        * attacker.stats[1]
                        / defender.stats[2]
                        / 50
                    )
                    * state_info["burn"]
                    * state_info["reflect"]
                    * state_info["weather"]
                    * state_info["flashfire"]
                    + 2
                )
                * state_info["stockpile"]
                * state_info["crit"]
                * state_info["doubledamage"]
                * state_info["charge"]
                * state_info["stab"]
                * type_chart_gen5(move["type"], defender.types)
            )
            damage_low: float = damage_high * 0.85
        else:
            state_info = get_info_gen_3(attacker, info, move)
            damage_high: float = (
                (
                    (
                        (2 * attacker.level / 5 + 2)
                        * move["power"]
                        * attacker.stats[3]
                        / defender.stats[4]
                        / 50
                    )
                    * state_info["burn"]
                    * state_info["light"]
                    * state_info["weather"]
                    * state_info["flashfire"]
                    + 2
                )
                * state_info["stockpile"]
                * state_info["crit"]
                * state_info["doubledamage"]
                * state_info["charge"]
                * state_info["stab"]
                * type_chart_gen5(move["type"], defender.types)
            )
            damage_low: float = damage_high * 0.85
    x = {"sand": "rock", "hail": "ice"}
    if info["weather"] in x.keys() and x[info["weather"]] not in defender.types:
        return f"{ceil(damage_low / defender.stats[0] * 100)}% - {ceil(damage_high / defender.stats[0] * 100)}% + 6.25% Rock or Hail"
    else:
        return ceil(damage_low / defender.stats[0] * 100), ceil(
            damage_high / defender.stats[0] * 100
        )


def get_info_gen_3(attacker: Pokemon, info: dict, move: dict):
    List = [
        "burn",
        "reflect",
        "light",
        "flashfire",
        "weather",
        "stockpile",
        "crit",
        "doubledamage",
        "charge",
        "stab",
    ]
    for x in List:
        if x not in info.keys():
            info[x] = False
    damage_info: dict = {}
    if info["burn"]:
        if move["category"] == "physical":
            damage_info["burn"] = 0.5
        else:
            damage_info["burn"] = 1
    else:
        damage_info["burn"] = 1
    if info["reflect"]:
        damage_info["reflect"] = 0.5
    else:
        damage_info["reflect"] = 1
    if info["light"]:
        damage_info["light"] = 0.5
    else:
        damage_info["light"] = 1
    if info["flashfire"]:
        if move["type"] == "fire":
            damage_info["flashfire"] = 1.5
        else:
            damage_info["flashfire"] = 1
    else:
        damage_info["flashfire"] = 1
    damage_info["weather"] = weather_calc_gen3(info["weather"], move)
    damage_info["stockpile"] = info["stockpile"]
    if info["stockpile"] == False:
        damage_info["stockpile"] = 1
    if info["crit"]:
        damage_info["crit"] = 2
    else:
        damage_info["crit"] = 1
    if info["doubledamage"]:
        damage_info["doubledamage"] = 2
    else:
        damage_info["doubledamage"] = 1
    if info["charge"]:
        if move["type"] == "electric":
            damage_info["charge"] = 2
        else:
            damage_info["charge"] = 1
    else:
        damage_info["charge"] = 1
    if move["type"] in attacker.types:
        damage_info["stab"] = 1.5
    else:
        damage_info["stab"] = 1
    return damage_info


def get_info_gen_3_doubles(attacker: Pokemon, info: dict, move: dict):
    List = [
        "burn",
        "reflect",
        "light",
        "flashfire",
        "weather",
        "stockpile",
        "crit",
        "doubledamage",
        "charge",
        "stab",
        "enemies",
        "allies",
        "helpinghand",
    ]
    for x in List:
        if x not in info.keys():
            info[x] = False
    damage_info: dict = {}
    if info["burn"]:
        if move["category"] == "physical":
            damage_info["burn"] = 0.5
        else:
            damage_info["burn"] = 1
    else:
        damage_info["burn"] = 1
    if info["reflect"]:
        if info["crit"]:
            damage_info["reflect"] = 1
        else:
            damage_info["reflect"] = 0.67
    else:
        damage_info["reflect"] = 1
    if info["light"]:
        if info["crit"]:
            damage_info["light"] = 1
        else:
            damage_info["light"] = 0.67
    else:
        damage_info["light"] = 1
    damage_info["targets"] = get_target_mult(move, info)
    if info["flashfire"]:
        if move["type"] == "fire":
            damage_info["flashfire"] = 1.5
        else:
            damage_info["flashfire"] = 1
    else:
        damage_info["flashfire"] = 1
    damage_info["weather"] = weather_calc_gen3(info["weather"], move)
    damage_info["stockpile"] = info["stockpile"]
    if info["stockpile"] == False:
        damage_info["stockpile"] = 1
    if info["crit"]:
        damage_info["crit"] = 2
    else:
        damage_info["crit"] = 1
    if info["doubledamage"]:
        damage_info["doubledamage"] = 2
    else:
        damage_info["doubledamage"] = 1
    if info["charge"]:
        if move["type"] == "electric":
            damage_info["charge"] = 2
        else:
            damage_info["charge"] = 1
    else:
        damage_info["charge"] = 1
    if info["helpinghand"]:
        damage_info["helpinghand"] = 1.5
    else:
        damage_info["helpinghand"] = 1
    if move["type"] in attacker.types:
        damage_info["stab"] = 1.5
    else:
        damage_info["stab"] = 1
    return damage_info


def weather_calc_gen3(weather: str, move: dict) -> int:
    match (weather):
        case "sun":
            if move["type"] == "fire":
                return 1.5
            if move["type"] == "water":
                return 0.5
            return 1
        case "rain":
            if move["type"] == "water":
                return 1.5
            if move["type"] == "fire":
                return 0.5
            return 1
        case _:
            return 1


def get_target_mult(move: dict, info: dict) -> int:
    match (move["target"]):
        case "all-other-pokemon":
            if (info["enemies"] + info["allies"]) > 1:
                return 0.5
        case "all-opponents":
            if info["enemies"] > 1:
                return 0.5
    return 1


def type_chart_gen5(att_type: str, def_types: list[str]) -> float:
    with open("files/type_chart_5.json", "r") as file:
        type_data = json.load(file)
    row = type_data[att_type]
    if len(def_types) < 2:
        multiplier = row.get(def_types[0], 1)
    else:
        multiplier = row.get(def_types[0], 1)
        multiplier *= row.get(def_types[1], 1)
    return multiplier


def type_chart_gen6(att_type: str, def_types: list[str]) -> float:
    with open("files/type_chart_6.json", "r") as file:
        type_data = json.load(file)
    row = type_data[att_type]
    if len(def_types) < 2:
        multiplier = row.get(def_types[0], 1)
    else:
        multiplier = row.get(def_types[0], 1)
        multiplier *= row.get(def_types[1], 1)
    return multiplier


if __name__ == "__main__":
    # pokemon_1 = Pokemon.get_pokemon('snorlax', 'emerald')
    # pokemon_1.level = 75
    # pokemon_1.update()
    # print(pokemon_1)
    # pokemon_2 = Pokemon.get_pokemon("mewtwo", 'emerald')
    # print(pokemon_2)
    # pokemon_3 = Pokemon.get_pokemon('shiftry', 'emerald')
    # print(pokemon_3)
    # print(damage_gen3(pokemon_2, pokemon_3, 'fire-blast', 'emerald'))
    tester_1 = Pokemon.get_pokemon("snorlax", "emerald")
    tester_2 = Pokemon.get_pokemon("mewtwo", "emerald")
    tester_3 = Pokemon.get_pokemon("pidgey", "emerald")

    print(damage_gen3(tester_1, tester_2, "snarl", "emerald"))
    print(
        damage_gen3(
            tester_1,
            tester_2,
            "snarl",
            "emerald",
            {"double": True, "enemies": 2},
        )
    )
    print(damage_gen3(tester_2, tester_3, "fire-punch", "emerald"))
    print(
        damage_gen3(
            tester_2,
            tester_3,
            "thunder-punch",
            "emerald",
        )
    )
