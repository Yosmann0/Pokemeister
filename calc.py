


class Pokemon():
    def __init__(self, dex, name, abilities, moves, types, basestats):
        self.dex = dex
        self.name = name
        self.abilities = abilities
        self.level = 0
        self.moves = moves
        self.types = types
        self.basestats = basestats
        self.ivs = []
        self.evs = []
        self.gender = 'Genderless'
        self.nature = 'Docile'
        self.item = 'none'
        self.status = 'none'


Pokemon_1 = Pokemon(143, "snorlax", ["immunity", "thick-fat", "gluttony"], ["mega-punch"], ["normal"], [160, 110, 65, 65, 110, 30])
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
