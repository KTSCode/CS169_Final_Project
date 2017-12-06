# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from scipy.optimize import linear_sum_assignment
import random
import Pokemon

def moves_dict(pkms):
    moves = {}
    for i in range(len(pkms['Moves'])):
        moves[i] = pkms['Moves'][i]
    return moves


def opt_cost(col_ind, matrix):
    cost = []
    for i in range(len(col_ind)):
        cost.append(matrix[i][col_ind[i]])
    return cost

def n_vs_n(costs, moves, team, enemy, n):
    uni_hit_matrix = [[] for i in range(n)]
    for cost in costs:
        for i, c in enumerate(cost):
            uni_hit_matrix[i].append(c)
    row_ind, col_ind = linear_sum_assignment(uni_hit_matrix)
    for i, ind in enumerate(col_ind):
        pkm = Team_of_4[ind]['name']
        enemy = Enemy_of_4[i]['name']
        move_n = Pokemon.Moves[moves[ind][i]]['name']
        print "Uses {} with {} on {}".format(pkm, move_n, enemy)
    
# 1V4 optimization
pokemon_rand = random.sample(range(1, 800), 8)

Team_of_4 = [Pokemon.Pokemon[i] for i in pokemon_rand[:4]]
Enemy_of_4 = [Pokemon.Pokemon[i] for i in pokemon_rand[4:]]

moves_1 = moves_dict(Team_of_4[0])
hit_matrix = Pokemon.hitMatrixMaker(Enemy_of_4, Team_of_4[0], len(Enemy_of_4))
row_ind, col_ind = linear_sum_assignment(hit_matrix)
moves_1 = [moves_1[i] for i in col_ind]
print "1V4"
print "For "+ Team_of_4[0]['name']
for i in range(len(col_ind)):
    print "Uses "+Pokemon.Moves[moves_1[i]]['name'] +" on "+Enemy_of_4[i]['name'] 

opt_cost_1 = opt_cost(col_ind, hit_matrix)

#4V4 optimization

#second pkm
moves_2 = moves_dict(Team_of_4[1])
hit_matrix2 = Pokemon.hitMatrixMaker(Enemy_of_4, Team_of_4[1], len(Enemy_of_4))
row_ind, col_ind = linear_sum_assignment(hit_matrix2)
moves_2 = [moves_2[i] for i in col_ind]
opt_cost_2 = opt_cost(col_ind, hit_matrix2)
#third pkm
moves_3 = moves_dict(Team_of_4[2])
hit_matrix3 = Pokemon.hitMatrixMaker(Enemy_of_4, Team_of_4[2], len(Enemy_of_4))
row_ind, col_ind = linear_sum_assignment(hit_matrix3)
moves_3 = [moves_3[i] for i in col_ind]
opt_cost_3 = opt_cost(col_ind, hit_matrix3)
#fourth pkm
moves_4 = moves_dict(Team_of_4[3])
hit_matrix4 = Pokemon.hitMatrixMaker(Enemy_of_4, Team_of_4[3], len(Enemy_of_4))
row_ind, col_ind = linear_sum_assignment(hit_matrix4)
moves_4 = [moves_4[i] for i in col_ind]
opt_cost_4 = opt_cost(col_ind, hit_matrix4)

print "4V4"
n_vs_n([opt_cost_1, opt_cost_2, opt_cost_3, opt_cost_4], [moves_1, moves_2, moves_3, moves_4], Team_of_4, Enemy_of_4, 4)

