import pickle
import MCvsBaleze
import ia
from morpionMCenv import MorpionMCEnv

file = open("./ia/ia1_", "rb")
policy = pickle.load(file)
file.close()

file = open("./ia/ia2__5_5_5_1.0", "rb")
morpion_load = pickle.load(file)
file.close()

def check_win(move, player):
    """ Check is the current state is a winning stage

    :param move:
    :return reward, is it a final state
    """

    move_p0 = set()
    move_p1 = set()

    for c in range(len(move)):
        if c % 2 == 0:
            move_p0.add(move[c])
        else:
            move_p1.add(move[c])

    winning_states = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},
                      {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]

    for w_state in winning_states:

        if move_p0.issuperset(w_state):
            if player == 0:
                return move, MorpionMCEnv.WIN_VALUE, True
            else:
                return move, MorpionMCEnv.LOSS_VALUE, True

        if move_p1.issuperset(w_state):
            if player == 1:
                return move, MorpionMCEnv.WIN_VALUE, True
            else:
                return move, MorpionMCEnv.LOSS_VALUE, True

    if len(move) == 9:
        return move, MorpionMCEnv.DRAW_VALUE, True

    return move, MorpionMCEnv.DRAW_VALUE, False


def saisir_tuple(lastTuple):
    t = lastTuple
    c = input()
    t = t + (int(c),)
    return t

nextTup = ()
win = 0
lose = 0
draw = 0
for i in range(1000):
    while True:
        if nextTup in policy:
            action = MCvsBaleze.nextAction(policy[nextTup], 9)
        else:
            action = MCvsBaleze.nextAction(nextTup, 9)
        _, reward, done = check_win(nextTup, 0)
        if done:
            if reward == 50:
                draw += 1
            elif reward == 100:
                win += 1
            else:
                lose += 1
            break
        nextTup = nextTup + (action,)
        nextTup = ia.next_action(morpion_load, nextTup)
        _, reward, done = check_win(nextTup, 1)
        if done:
            if reward == 50:
                draw += 1
            elif reward == 100:
                lose += 1
            else:
                win += 1
            break

print('win : ', win, ' lose : ', lose, ' draw : ', draw)

