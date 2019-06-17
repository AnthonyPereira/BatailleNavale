import copy
import pickle
import sys
from collections import defaultdict
from random import randint

import numpy as np


def generate_episode_from_Q(env1, env2, Q1, Q2, epsilon, nA):
    """
    generates an episode from following the epsilon-greedy policy

    """
    episode1 = []
    episode2 = []

    state = env1.reset()
    cpt = 0
    while True:
        if cpt % 2 == 0:
            action = np.random.choice(np.arange(nA), p=get_probs(Q1[state], epsilon, nA))
            env1.addMove(action)
            next_state, reward, done = env1.check_win()
            episode1.append((state, action, reward))
        else:
            action = np.random.choice(np.arange(nA), p=get_probs(Q1[state], epsilon, nA))
            env1.addMove(action)
            next_state, reward, done = env2.check_win()
            episode2.append((state, action, reward))
        state = next_state
        cpt += 1
        if done:
            break
    return episode1, episode2


def get_probs(Q_s, epsilon, nA):
    """ obtains the action probabilities corresponding to epsilon-greedy policy """
    policy_s = np.ones(nA) * epsilon / nA
    best_a = np.argmax(Q_s)
    policy_s[best_a] = 1 - epsilon + (epsilon / nA)
    return policy_s


def update_Q_alpha(env1, episode, Q, alpha, gamma):
    """ updates the action-value function estimate using the most recent episode """
    states, actions, rewards = zip(*episode)
    # prepare for discounting
    discounts = np.array([gamma ** i for i in range(len(rewards) + 1)])
    for i, state in enumerate(states):
        old_Q = Q[state][actions[int(i)]]
        Q[state][actions[i]] = old_Q + alpha * (sum(rewards[i:] * discounts[:-(1 + i)]) - old_Q)
    return Q


def generateQRec(Q, env, move):
    """Initialize Q
    :param move:
    :return nothing:
    """

    state, reward, final_state = env.check_win(move)
    if final_state or len(move) == env.getNbSquare():
        return Q

    action = {}
    for mo in range(0, env.getNbSquare()):
        action[mo] = 0

    Q[move] = action

    for mo in range(0, env.getNbSquare()):
        Q = generateQRec(Q, env, move + (mo,))
    return Q


def generateQ(Q, env, move):
    Q = {(): {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}}
    Q = generateQRec(Q, env, move)

    return Q


def maxiDico(dico):
    max = None
    valMax = None
    for k, v in dico.items():
        if max == None or valMax < v:
            max = k
            valMax = v
    liste = []
    for k, v in dico.items():
        if valMax == v:
            liste.append(k)
    return np.random.choice(liste)


def mc_control_alpha(env1, env2, num_episodes, alpha, Q1, Q2, gamma=1.0):
    nA = env1.getNbSquare()
    # initialize empty dictionary of arrays
    # loop over episodes
    for i_episode in range(1, int(num_episodes) + 1):
        # monitor progress
        if i_episode % 1000 == 0:
            print(i_episode)
            sys.stdout.flush()
        # set the value of epsilon
        epsilon = 1.0 / ((i_episode / 8000) + 1)
        # generate an episode by following epsilon-greedy policy
        episode1, episode2 = generate_episode_from_Q(env1, env2, Q1, Q2, epsilon, nA)
        # update the action-value function estimate using the episode
        Q1 = update_Q_alpha(env1, episode1, Q1, alpha, gamma)
    # determine the policy corresponding to the final action-value function estimate
    policy = {}
    print("new policy")
    for k, v in Q1.items():
        policy[k] = {}
        for kv, vv in v.items():
            if vv > np.argmax(v) - 10:
                policy[k][kv] = vv
            else:
                policy[k][kv] = 0
    print(policy)
    return policy, Q1, Q2


def next_action(policy, state):
    return policy[state]


def save(policy, name):
    file = open(name, "wb")
    pickle.dump(policy, file)
