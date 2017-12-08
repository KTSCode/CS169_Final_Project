import Pokemon as P
import matrix as M
import numpy as np
import matplotlib.pyplot as plt

def VSix(ID):
    Team = P.genRandomTeam(151, 6)
    if ID == 0 :
        Pkm = P.genRandom(151)
    else:
        Pkm = ID, P.Pokemon[ID]
    V = P.hitMatrixMaker(Team[1], Pkm[1])
    Res = M.get_results(V, Team[0], Pkm[0])
    if(Res[0]):
        print("Attacking Pokemon:")
        print("\t" + Pkm[1]['name'])
        print("Defending Pokemon Team:")
        for i in range(6):
            print("\t" + Team[1][i]['name'])
        print("Moves To Choose:")
        for j in set(Res[2][1]):
            print("\t" + P.Moves[Pkm[1]['Moves'][j]]['name'])
    else:
        if ID == 0:
            VSix(0)
        else:
            print("We're sorry there was an error processing the pokemon you entered")
