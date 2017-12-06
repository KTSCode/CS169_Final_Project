import csv
from math import ceil
from random import randint
import numpy as np

# Define dictionary of Pokemon return Pokemon, Moves, Effectiveness
def makeDicts():
    global Pokemon
    global Moves
    global Effectiveness
    Pokemon = {0: {'name': '', 'type1': 0, 'type2': 0,
      'Attack': 0, 'Defense': 0, 'Special Attack': 0, 'Special Defense': 0, 'HP': 0,
      'Moves': [0]}}

    # Define dictionary of Moves
    Moves = {0: {'name': '', 'power': 0, 'type': 0, 'pp': 0, 'damage': 0}}

    # Define Effectiveness matrix
    typeNum = 19 #I'm lazy and didn't want to convert to start at 0
    Effectiveness = [[1 for x in range(typeNum)] for y in range(typeNum)]

    # Add names to pokemon dict
    with open('pokemon.csv', 'r') as csvfile:
      reader = csv.DictReader(csvfile   )
      for row in reader:
        if row['is_default'] == '1':
          Pokemon[int(row['id'])] = {'name': row['identifier'], 'type1': 0, 'type2': 0,
            'Attack': 1, 'Defense': 1, 'Special Attack': 1, 'Special Defense': 1, 'HP': 1,
            'Moves': set([]) }

    # Add types to pokemon dict
    with open('pokemon_types.csv', 'r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        id = int(row['pokemon_id'])
        if id < len(Pokemon):
          if row['slot'] == '1':
            Pokemon[id]['type1'] = int(row['type_id'])
          else:
            Pokemon[id]['type2'] = int(row['type_id'])

    # Add stats to pokemon dict
    with open('pokemon_stats.csv', 'r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        id = int(row['pokemon_id'])
        if id < len(Pokemon):
          if row['stat_id'] == '1':
            Pokemon[id]['HP'] = int(row['base_stat'])
          if row['stat_id'] == '2':
            Pokemon[id]['Attack'] = int(row['base_stat'])
          if row['stat_id'] == '3':
            Pokemon[id]['Defense'] = int(row['base_stat'])
          if row['stat_id'] == '4':
            Pokemon[id]['Special Attack'] = int(row['base_stat'])
          if row['stat_id'] == '5':
            Pokemon[id]['Special Defense'] = int(row['base_stat'])

    # Add moves to pokemon dict
    with open('pokemon_moves1.csv', 'r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        ID = int(row['pokemon_id'])
        if ID < len(Pokemon):
          Pokemon[ID]['Moves'].add(int(row['move_id']))
      for pokemon_id in Pokemon:
          Pokemon[ID]['Moves']=list(Pokemon[ID]['Moves'])

    # Add moves to Moves dict
    with open('moves.csv', 'r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        power = 0 if row['power'] == '' else int(row['power'])
        pp = 0 if row['pp'] == '' else int(row['pp'])
        type_id = 0 if row['type_id'] == '' else int(row['type_id'])
        damage = 0 if row['damage_class_id'] == '' else int(row['damage_class_id'])
        # for damage 0=notfound 1=status 2=physical 3=special
        Moves[int(row['id'])] = {'name': row['identifier'], 'power': power,
          'type': type_id, 'pp': pp, 'damage': damage}

    # Add Type efficacy to Effectiveness matrix
    with open('type_efficacy.csv', 'r') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        damage_type = int(row['damage_type_id'])
        target_type = int(row['target_type_id'])
        damage = 0 if row['damage_factor'] == '' else int(row['damage_factor'])
        if damage == 0:
          Effectiveness[damage_type][target_type] = damage
        if damage == 100:
          Effectiveness[damage_type][target_type] = 1
        if damage == 50:
          Effectiveness[damage_type][target_type] = 0.5
        if damage == 200:
          Effectiveness[damage_type][target_type] = 2
    return Pokemon, Moves, Effectiveness
# Calculate damage done to a pokemon
# int *args -> int
def damageCalc(level, power, attack, defense, mod):
  atk = int(((attack * 2 + 31) * level / 100) + 5)
  _def = int(((defense * 2 + 31) * level / 100) + 5)
  # I was having trouble makeing it work, so I broke it down by step
  a = 2 * level
  b =  float(a) / 5.0
  c = b + 2.0
  d = c * float(power)
  e = float(atk) / float(_def)
  f = d * e
  g = f / 50.0
  h = g + 2.0
  i = h * mod
  return int(i)

# Calculate number of attacks by atk_pkm to def_pkm with move
# it takes to KO def_pkm
# Pokemon(dict) atk_pkm, Pokemon(dict) def_pkm, Move(dict) move -> int
def hitsToKO(atk_pkm, def_pkm, move):
  # Calc Effectivness
  mod = Effectiveness[move['type']][def_pkm['type1']] * Effectiveness[move['type']][def_pkm['type2']]
  # Calc STAB
  if atk_pkm['type1'] == move['type'] or atk_pkm['type2'] == move['type']:
    mod = mod * 1.5
  # Calc attack and defense based on move damage type
  if move['damage'] == 2:
    defense = def_pkm['Defense']
    attack = atk_pkm['Attack']
  elif move['damage'] == 3:
    defense = def_pkm['Special Defense']
    attack = atk_pkm['Special Attack']
  else:
    return np.inf # notfound moves and status moves will never kill a pokemon

  level = 100
  # Calc Damage
  damage = damageCalc(level, move['power'], attack, defense, mod)
  if damage == 0:
    return np.inf
  # Assuming all pokemons IVs are 31 and EVs are 0
  hp = ((def_pkm['HP'] * 2 + 31 ) * level / 100) + 10 + level

  #TODO for testing purposes remove later
  # print atk_pkm['name'] + ' attacks ' + def_pkm['name'] + ' using ' + move['name']
  # print 'mod: ' + str(mod)
  # print "damage: " + str(damage)
  # print "HP: " + str(hp)

  #return number of hits to KO rounding up
  return ceil(float(hp)/float(damage))

# Hits Matrix
def hitMatrixMaker(team, atk_pkm):
  ht = len(team)
  #for move in atk_pkm['Moves']:
  #  print(move,Moves[move]['power'])
  atk_pkm['Moves']= [move for move in atk_pkm['Moves'] if Moves[move]['power']>0]

  wt = len(atk_pkm['Moves'])
  HitsMatrix = [[100 for x in range(wt)] for y in range(ht)]
  for i in range(ht):
    for j in range(wt):
      HitsMatrix[i][j] = hitsToKO(atk_pkm, team[i], Moves[list(atk_pkm['Moves'])[j]])
  return HitsMatrix
def genRandomTeam(max_pokemon=151, num =6):
    ids = [randint(1,max_pokemon) for i in range(num)]
    Team = [Pokemon[id] for id in ids]
    return ids, Team
def genRandom(max_pokemon=151):
    num = randint(1,max_pokemon)
    return num, Pokemon[num]
def randomArray(max_pokemon=151):
    team_ids, Team = genRandomTeam(max_pokemon)
    atk_id, Pokem = genRandom(max_pokemon)
    return atk_id, team_ids, hitMatrixMaker(Team,Pokem)
#print(np.array(hitMatrixMaker(Team, atk_pkm)))
  # print hitsToKO(Pokemon[randint(1,max_pokemon)], Pokemon[randint(1,max_pokemon)], Moves[randint(1,600)])
