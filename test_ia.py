import pickle
import ia

file = open("./ia/ia1__5_5_5_1.0", "rb")
morpion_load = pickle.load(file)


def saisir_tuple(lastTuple):
    t = lastTuple
    c = input()
    t = t + (int(c),)
    return t

allumetteEnleve=0
tup=()
nextTup=()
while True:
    nextTup = ia.next_action(morpion_load, tup)
    print(morpion_load.policy[tup])
    print(nextTup)

    if allumetteEnleve==9:
        rejouer=input("voulez vous rejouer (y/n) : ")
        if rejouer=='n':
            break
        else :
            tup = ()
            nextTup = ()
    print("saisir action : ")
    tup = saisir_tuple(nextTup)




