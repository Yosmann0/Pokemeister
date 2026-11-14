import pytest
from backend.calc import Pokemon, damage_gen3
from backend.data import *
import sys

relaxo = Pokemon.get_pokemon("snorlax", "emerald")
mewtwo = Pokemon.get_pokemon("mewtwo", "emerald")
taubsi = Pokemon.get_pokemon("pidgey", "emerald")


def gen_3_double_battle_drop(attacker, defender):
    single_low, single_high = damage_gen3(attacker, defender, "surf", "emerald")
    double_low, double_high = damage_gen3(
        attacker, defender, "surf", "emerald", {"double": True, "enemies": 2}
    )
    return single_low, single_high, double_low, double_high


def test_gen_3_double_battle_drop():
    single_low, single_high, double_low, double_high = gen_3_double_battle_drop(
        relaxo, mewtwo
    )
    assert single_low > double_low and single_high > double_high


def gen_3_type_chart(attacker, defender):
    effective_low, effective_high = damage_gen3(
        attacker, defender, "fire-punch", "emerald"
    )
    supereffective_low, supereffective_high = damage_gen3(
        attacker, defender, "thunder-punch", "emerald"
    )
    return effective_low, effective_high, supereffective_low, supereffective_high


def test_gen_3_type_chart():
    effective_low, effective_high, supereffective_low, supereffective_high = (
        gen_3_type_chart(mewtwo, taubsi)
    )
    assert effective_low < supereffective_low and effective_high < supereffective_high


def gen_3_weather(attacker, defender):
    no_low, no_high = damage_gen3(attacker, defender, "fire-punch", "emerald")
    sun_low, sun_high = damage_gen3(
        attacker, defender, "fire-punch", "emerald", {"weather": "sun"}
    )
    rain_low, rain_high = damage_gen3(
        attacker, defender, "fire-punch", "emerald", {"weather": "rain"}
    )
    return no_low, no_high, sun_low, sun_high, rain_low, rain_high


def test_gen_3_weather():
    no_low, no_high, sun_low, sun_high, rain_low, rain_high = gen_3_weather(
        mewtwo, taubsi
    )
    assert rain_low < no_low < sun_low and rain_high < no_high < sun_high
