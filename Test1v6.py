import Pokemon as P
import matrix as M
import numpy as np
import matplotlib.pyplot as plt

def Test():
    Team = P.genRandomTeam(151, 6)
    Pkm = P.genRandom(151)
    # Pkm = 40, P.Pokemon[40]
    V = P.hitMatrixMaker(Team[1], Pkm[1])
    Res = M.get_results(V, Team[0], Pkm[0])
    return len(Pkm[1]['Moves']), Res[0]

Pass = np.zeros(500)
Fail = np.zeros(500)
for i in range(200):
  # print(str(i) + ", ")
  test = Test()
  # print(test)
  if(test[1]):
      Pass[int(test[0])] += 1
  else:
      Fail[int(test[0])] += 1


Ratios = []
MoveCount = []
PF = []
for i in range(500):
    if (Pass[i] + Fail[i]) < 2:
      continue
    if Fail[i] != 0 :
        PF.append(( Pass[i] + Fail[i] )/100)
        MoveCount.append(i)
        Ratios.append(Pass[i]/(Pass[i] + Fail[i]))
    elif Pass[i] != 0 :
        PF.append(( Pass[i] + Fail[i] )/100)
        MoveCount.append(i)
        Ratios.append(Pass[i]/(Pass[i] + Fail[i]))
print(MoveCount)
print(Ratios)
print(PF)
plt.plot(MoveCount, Ratios, "ro")
plt.errorbar(MoveCount, Ratios, yerr=PF, ecolor='tab:red')
plt.axis([0, max(MoveCount) + 1, -0.01, 1.1])
plt.ylabel('some numbers')
plt.show()
    # if(Res[0]):
        # print("Attacking Pokemon:")
        # print("\t" + Pkm[1]['name'])
        # print("Defending Pokemon Team:")
        # for i in range(6):
            # print("\t" + Team[1][i]['name'])
        # print("Moves To Choose:")
        # for j in set(Res[2][1]):
            # print("\t" + P.Moves[Pkm[1]['Moves'][j]]['name'])
    # else:
        # print(Res[1])

# Test()
