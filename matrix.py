import numpy as np
from math import factorial as f
import scipy.optimize as opt
import matplotlib.pyplot as plt
import Pokemon as P
import csv

def make_EQ(I,J):
    tests = []
    values = []
    #Procedure to check all I rows' sum
    #I tests
    checkRows = np.zeros((I,I,J))
    for i in range(I):
        checkRows[i,i,:]=np.ones(J)
        tests.append(checkRows[i].flatten())
        values.append(1)
    #check all J cols' sum
    #J tests
    checkCols = np.zeros((J,I,J))
    for j in range(J):
        checkCols[j,:,j]=np.ones(I)
        temp = np.zeros(I*J+J)
        temp[:I*J]=checkCols[j].flatten() #sum of col
        temp[I*J+j]=-1 #substracting k_j
        tests.append(temp)
        values.append(0)
    # check sum of Kj
    # 1 test
    temp = np.zeros(I*J+J)
    temp[I*J:]=np.ones(J)
    tests.append(temp)
    values.append(6)
    # check sum of Cj
    # 1 test
    temp = np.zeros(I*J+2*J)
    temp[I*J+J:]=np.ones(J)
    tests.append(temp)
    values.append(4)
    #check sum of whole thing
    temp = np.ones(I*J)
    tests.append(temp)
    values.append(6)
    matrix = turn_to_matrix(tests)
    #print(matrix.shape,len(values))
    return matrix, values
def make_UB(I,J):
    tests = []
    values = []
    #check C_j less than k_j
    for j in range(J):
        checkCK = np.zeros((I*J+2*J))
        checkCK[I*J+j]=-1
        checkCK[I*J+J+j]=1
        tests.append(checkCK.flatten())
        values.append(0)
    #check k_j less than 3*C_j
    for j in range(J):
        checkCK = np.zeros((I*J+2*J))
        checkCK[I*J+j]=1
        checkCK[I*J+J+j]=-3
        tests.append(checkCK.flatten())
        values.append(0)
    matrix = turn_to_matrix(tests)
    return matrix,values
def turn_to_matrix(ls):
    lens = [len(row) for row in ls]
    #print(lens)
    matrix = np.zeros((len(ls),max(lens)))
    for i, row in enumerate(ls):
        matrix[i,:lens[i]]=row
    return np.array(matrix)

def make_bounds(I,J):
    #bound x (0,1)
    bounds = [(0,1)]*I*J+[(0,3)]*J+[(0,1)]*J
    return bounds

def make_solver(v):
    v = np.array(v)
    #print(v,v.shape)
    I,J = v.shape
    A_eq, b_eq = make_EQ(I,J)
    A_ub, b_ub = make_UB(I,J)
    #print("eq:",A_eq.shape,"ub",A_ub.shape)
    bounds = make_bounds(I,J)
    v_f = np.zeros(I*J+2*J)
    #print("v_f",v_f.shape)
    v_f[:I*J] = v.flatten()
    ans = opt.linprog(v_f,A_ub,b_ub,A_eq,b_eq,bounds)
    x = np.array(ans.x[:I*J]).reshape(v.shape)
    k = ans.x[I*J:-13]
    c = ans.x[-13:]
    return ans.success, x, v, k, c

def get_results(v, team_ids,atk_id):
    success = True
    msg = ""
    try:
        success, x,v,k,c= make_solver(v)
    except Exception as e:
        #print(e)
        success = False
        msg = "We cant process this pokemon"
        return success, msg, []
    selected = ((x+0.1)>1).astype(int)
    enemy, moves = np.where(selected==1)
    if(sum(sum(selected))<6):
        msg = "We cant fully process this pokemon, but these are suggestion"
        success = False
    return success, msg, [enemy,moves,selected]
def get_results_movenames(v, team_ids,atk_id):
    success = True
    msg = ""
    try:
        success, x,v,k,c= make_solver(v)
    except Exception as e:
        #print(e)
        success = False
        msg = "We cant process this pokemon"
        return success, msg, []
    selected = ((x+0.1)>1).astype(int)
    enemy, moves = np.where(selected==1)
    move_ids = [Pokemon[atk_id]['Moves'][move] for move in moves]
    if(sum(sum(selected))<6):
        msg = "We cant fully process this pokemon, but these are suggestion"
        success = False
    return success,[enemy,move_ids]
def random_runner():
    exec(open('Pokemon.py').read())
    # Pokemon, Moves, Effectiveness = P.makeDicts()
    atk_id, team_ids, v = P.randomArray()
    s, msg, data = get_results(v,team_ids,atk_id)
    return s, msg, data, atk_id, team_ids, v
def stat_collector(tests):
    stats = {}
    trials = list([])
    for j in range(tests):
        type_e = 0
        s, msg, data, atk_id, teams_ids,v = random_runner()
        if not s :
            if len(data)==0:
                type_e =2
            else:
                out = check_if_undecideable(data[2],v,data[0])
                if (not len(out)==0) and ((len(out)==1 and len(out[0])>1) or (len(out)==2 and len(out[0])>1 and len(out[1])>1)):
                    type_e = 1
                else:
                    type_e = 2
        num_moves = len(Pokemon[atk_id]['Moves'])
        trials.append({'atk_id':atk_id,'teams_ids':teams_ids,'type_r':type_e,'moves':num_moves})
        stats[num_moves]=stats.get(num_moves,{'success':0,'total':0,'und':0})
        stats[num_moves]['total']+=1
        if(type_e == 0):
            stats[num_moves]['success']+=1
        elif(type_e == 1):
            stats[num_moves]['und']+=1
    return stats,trials
def stat_interpreter(stats):
    x=np.zeros(len(stats.keys()))
    y=np.zeros(len(stats.keys()))
    err = np.zeros(len(stats.keys()))
    comb = f(151) / f(6) / f(151-6)
    # print(comb)
    for i,k in enumerate(sorted(stats.keys())):
        x[i]=k
        y[i]=stats[k]['success']/stats[k]['total']
        # print (x[i],y[i])
        err[i]=calc_error(stats[k]['success'],stats[k]['total'])
    return x, y, err
def calc_error(s,n):
    t =(s+1/2)/(n+1)
    return np.sqrt(((1-t)*t)/(n+1))
def make_plot(x,y,e):
    plt.figure()
    plt.errorbar(x,y,yerr=e,capthick=2)
    plt.axis([0,40,0,1])
    plt.ylabel('Success Rate to Find Moves')
    plt.xlabel('Number of Damaging Moves Available')
    plt.title('Changes in Success Rate of Simplex Algorithm Depending on Pokemon\'s Moveset')
    plt.show()
def gen_plot(tests):
    stats, trials = stat_collector(tests)
    x,y,e = stat_interpreter(stats)
    make_plot(x,y,e)
    return x,y,e
def check_if_undecideable(selected, m, pokemon_killed):
    covered = [max(selected[:,i]) for i in range(len(selected[0]))]
    if sum(covered)<4:
        return []
    missing = [n for n in np.arange(6) if not( n in pokemon_killed)]
    solutions = []
    for missed in missing:
        available = np.array(covered[missed]*m[ missed])
        if(sum(available)==0):
            return []
        minimum = np.min([x for x in available if x>0])
        t = np.array(available==minimum).astype(int)
        count = sum(t)
        solutions.append(np.where(available==minimum))
    return solutions
