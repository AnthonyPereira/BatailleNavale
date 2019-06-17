import pickle
import ia

file = open("./ia/ia1__5_5_5_1.0", "rb")
morpion_load = pickle.load(file)
file.close()


def saisir_tuple(lastTuple):
    t = lastTuple
    c = input()
    t = t + (int(c),)
    return t


tup = ()
while True:
    nextTup = ia.next_action(morpion_load, tup)
    print(morpion_load.policy[tup])
    print(nextTup)
    tup = saisir_tuple(nextTup)

