import numpy as np
import scipy.optimize as opt
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
        selected = ((x+0.1)>1).astype(int)
        enemy, moves = np.where(selected==1)
        if(sum(sum(selected))<6):
            msg = "We cant fully process this pokemon, but these are suggestion"
            success = False

        return success, msg, [enemy,moves]
    except Exception as e:
        print(e)
        success = False
        msg = "We cant process this pokemon"
        return success, msg, []

def random_runner():
    exec(open('Pokemon.py').read())
    Pokemon, Moves, Effectiveness = makeDicts()
    atk_id, team_ids, v = randomArray()
    s, msg, data = get_results(v,team_ids,atk_id)
    return s, msg, data, atk_id, team_ids
