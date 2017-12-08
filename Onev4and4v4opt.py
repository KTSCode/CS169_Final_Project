from scipy.optimize import linear_sum_assignment
import random
import Pokemon
import numpy as np
import matplotlib.pyplot as plt

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
        print("\tUse {} with {} on {}".format(move_n, pkm, enemy))
# 6v6
def SixVSix():
    pokemon_rand = random.sample(range(1, 152), 12)
    Team_of_6 = [Pokemon.Pokemon[i] for i in pokemon_rand[:4]]
    Enemy_of_6 = [Pokemon.Pokemon[i] for i in pokemon_rand[4:]]
    #TODO Add Code Here

# 1V4 optimization

def VFour(One):
    pokemon_rand = random.sample(range(1, 152), 8)
    global Team_of_4
    Team_of_4 = [Pokemon.Pokemon[i] for i in pokemon_rand[:4]]
    global Enemy_of_4
    Enemy_of_4 = [Pokemon.Pokemon[i] for i in pokemon_rand[4:]]

    hit_matrix = Pokemon.hitMatrixMaker(Enemy_of_4, Team_of_4[0])
    moves_1 = Team_of_4[0]['Moves']
    #print(np.matrix(hit_matrix))
    row_ind, col_ind = linear_sum_assignment(hit_matrix)
    moves_1 = [moves_1[i] for i in col_ind]
    opt_cost_1 = opt_cost(col_ind, hit_matrix)
    if One :
        print("1V4:")
        print("For "+ Team_of_4[0]['name'])
        if len(col_ind) < 4 :
            print("This pokemon can only learn " + str(len(col_ind)) + " attacking move(s).")
        for i in range(len(col_ind)):
            print("\tUse "+Pokemon.Moves[moves_1[i]]['name'] +" on "+Enemy_of_4[i]['name'])
    else:
        #4V4 optimization
        #second pkm
        hit_matrix2 = Pokemon.hitMatrixMaker(Enemy_of_4, Team_of_4[1])
        moves_2 = Team_of_4[1]['Moves']
        row_ind, col_ind = linear_sum_assignment(hit_matrix2)
        moves_2 = [moves_2[i] for i in col_ind]
        opt_cost_2 = opt_cost(col_ind, hit_matrix2)
        #third pkm
        hit_matrix3 = Pokemon.hitMatrixMaker(Enemy_of_4, Team_of_4[2])
        moves_3 = Team_of_4[2]['Moves']
        row_ind, col_ind = linear_sum_assignment(hit_matrix3)
        moves_3 = [moves_3[i] for i in col_ind]
        opt_cost_3 = opt_cost(col_ind, hit_matrix3)
        #fourth pkm
        hit_matrix4 = Pokemon.hitMatrixMaker(Enemy_of_4, Team_of_4[3])
        moves_4 = Team_of_4[3]['Moves']
        row_ind, col_ind = linear_sum_assignment(hit_matrix4)
        moves_4 = [moves_4[i] for i in col_ind]
        opt_cost_4 = opt_cost(col_ind, hit_matrix4)
        print("4V4:")
        n_vs_n([opt_cost_1, opt_cost_2, opt_cost_3, opt_cost_4], [moves_1, moves_2, moves_3, moves_4], Team_of_4, Enemy_of_4, 4)

def Test():
    pokemon_rand = random.sample(range(1, 152), 8)
    Team_of_4 = [Pokemon.Pokemon[i] for i in pokemon_rand[:4]]
    Enemy_of_4 = [Pokemon.Pokemon[i] for i in pokemon_rand[4:]]
    hit_matrix = Pokemon.hitMatrixMaker(Enemy_of_4, Team_of_4[0])
    moves_1 = Team_of_4[0]['Moves']
    row_ind, col_ind = linear_sum_assignment(hit_matrix)
    moves_1 = [moves_1[i] for i in col_ind]
    return len(Team_of_4[0]['Moves']), len(col_ind) == 4

def plot(tests):
    Pass = np.zeros(500)
    Fail = np.zeros(500)
    for i in range(tests):
      if i == 0:
        print(str(i), end='')
      elif i < 10:
        print('\b' , end='', flush=True)
        print(str(i), end='')
      elif i < 100:
        print('\b\b', end='', flush=True)
        print(str(i), end='')
      elif i < 1000:
        print('\b\b\b', end='', flush=True)
        print(str(i), end='')
      elif i < 10000:
        print('\b\b\b', end='', flush=True)
        print(str(i), end='')
      test = Test()
      if(test[1]):
          Pass[int(test[0])] += 1
      else:
          Fail[int(test[0])] += 1

    def calc_error(s,n):
        t =(s+1/2)/(n+1)
        return np.sqrt(((1-t)*t)/(n+1))

    Ratios = []
    MoveCount = []
    PF = []
    for i in range(500):
        if Fail[i] != 0 :
            PF.append(calc_error(Pass[i], ( Pass[i] + Fail[i] )))
            MoveCount.append(i)
            Ratios.append(Pass[i]/(Pass[i] + Fail[i]))
        elif Pass[i] != 0 :
            PF.append(calc_error(Pass[i], ( Pass[i] + Fail[i] )))
            MoveCount.append(i)
            Ratios.append(1)
    plt.plot(MoveCount, Ratios, "ro")
    plt.errorbar(MoveCount, Ratios, yerr=PF, ecolor='tab:red')
    plt.axis([0, max(MoveCount) + 1, -0.01, 1.1])
    plt.ylabel('Percentage of Success Selecting Optimal Moves')
    plt.title('Change in Success Rate By Moves Available:  Linear Assignment')
    plt.xlabel('Number of Damaging Moves Availble to Pokemon')
    plt.show()

