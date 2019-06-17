import pickle
import MCvsBaleze
from morpionMCenv import MorpionMCEnv

file = open("./ia/ia1_", "rb")
policy = pickle.load(file)


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

while True:
    _, reward, done = check_win(nextTup, 1)
    if done:
        print(reward)
        break
    if nextTup in policy:
        print(policy[nextTup])
        action = MCvsBaleze.nextAction(policy, 9, nextTup)
    else:
        action = MCvsBaleze.nextAction(nextTup, 9, nextTup)
    nextTup = nextTup + (action,)
    print()
    print(nextTup)
    _, reward, done = check_win(nextTup, 0)
    if done:
        print(reward)
        break
    nextTup = saisir_tuple(nextTup)