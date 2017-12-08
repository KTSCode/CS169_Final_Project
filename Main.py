import Pokemon as P
import matrix as M
import Onev4and4v4opt as O
import Test1v6 as T
import sys

def Options(random):
    while True:
        print()
        print("Select a Format: ")
        print()
        print("\t1. 1v6" )
        if random: print("\t2. 6v6")
        if random: print("\t3. 4v4")
        if random: print("\t4. 1v4")
        print("\t5. Go Back" )
        print()
        choice2 = input ("Enter the number of your selection: ")
        if choice2 == "5":
            return
        elif choice2 == "1":
            if random :
                T.VSix(0)
            else:
                T.VSix(int(input ("Enter the id of the pokemon whose moveset you want to optimize: ")))
        elif choice2 == "2":
            O.SixVSix()
        elif choice2 == "3":
            O.VFour(False)
        elif choice2 == "4":
            O.VFour(True)
        else:
            print("I don't understand your choice.")

while True:
    print()
    print("Pokemon Move Set Optimizer: ")
    print()
    print("\t1. Enter the ids of the pokemon you want to test")
    print("\t2. Randomly select pokemon")
    print("\t3. Plot success rate for 1v4")
    print("\t4. Plot success rate for 1v6")
    print("\t5. Exit" )
    print()

    choice = input ("Enter the number of your selection: ")

    if choice == "5":
        sys.exit()
    elif choice == "1":
        Options(False)
    elif choice == "2":
        Options(True)
    elif choice == "3":
        O.plot(int(input ("Enter the number of tests you want to run: ")))
    elif choice == "4":
        M.gen_plot(int(input ("Enter the number of tests you want to run: ")))
    else:
        print("I don't understand your choice.")


