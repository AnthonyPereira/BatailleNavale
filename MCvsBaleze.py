import os
import sys
import numpy as np
import pickle
import ia


def saveQ(file_name, Q):
    file = open(file_name, "wb")
    pickle.dump(Q, file)
    file.close()


def nextAction(Q, nA, state):
    strat = []
    if type(Q) is tuple:
        for i in range(nA):
            if i not in Q:
                strat.append(1/(nA-len(Q)))
            else:
                strat.append(0)
    else:
        strat = get_probs(state, Q[state], 0, nA)
    return np.random.choice(np.arange(nA), p=strat)


def foundMinimumValue(k, v):
    reward = None
    value = None
    for i in range(len(v)):
        if i not in k and (reward is None or v[i] < reward):
            reward = v[i]
            value = i
    return value, reward


def max(state, Q_s, nA):
    maxValue = None
    maxAction = None
    for i in range(0, nA):
        if i not in state and (maxValue is None or maxValue < Q_s[i]):
            maxValue = Q_s[i]
            maxAction = i
    return maxAction


def get_probs(state, Q_s, epsilon, nA):
    """ obtains the action probabilities corresponding to epsilon-greedy policy """
    policy_s = np.ones(nA) * epsilon / (nA - len(state))
    best_a = max(state, Q_s, nA)
    policy_s[best_a] = 1 - epsilon + (epsilon / (nA - len(state)))
    for i in range(nA):
        if i in state:
            policy_s[i] = 0
    return policy_s


def generate_episode_from_Q(env1, env2, epsilon, nA, joueur, Q):
    """
    generates an episode from following the epsilon-greedy policy

    """
    episode = []
    state = env1.reset()
    cpt = 0
    while True:
        if cpt % 2 == 0:
            action = np.random.choice(np.arange(nA),
                                      p=get_probs(state, Q[state], epsilon, nA)) if state in Q else env1.getRandom(state)

            _, reward, done = env1.check_win(state + (action,))

        else:
            action = ia.next_action(env2, state)
            _, reward, done = env1.check_win(state + (action,), player=1)

        if joueur == cpt % 2:
            episode.append((state, action, reward))
        cpt += 1
        state += (action, )
        if len(state) > 1:
            if len(state) % 2 == 0:
                state = state[len(state)-1]
        if done:
            if joueur == cpt % 2:
                episode[len(episode) - 1] = (state[:len(state) - 2], state[len(state)-1:], -reward)
            break
    env1.reset()
    return episode


def update_Q_alpha(episode, alpha, gamma, Q, nA):
    """ updates the action-value function estimate using the most recent episode """
    states, actions, rewards = zip(*episode)
    # prepare for discounting
    discounts = np.array([gamma ** i for i in range(len(rewards) + 1)])
    for i, state in enumerate(states):
        if state not in Q:
            Q[state] = []
            for j in range(nA):
                Q[state].append(0)
            old_Q = Q[state][actions[i]]
        else:
            old_Q = Q[state][actions[i]]
        Q[state][actions[i]] = old_Q + alpha * (sum(rewards[i:] * discounts[:-(1 + i)]) - old_Q)


def mc_control_alpha(env1, env2, num_episodes, alpha, nA, Q, joueur, gamma=1.0):
    # loop over episodes
    for i_episode in range(1, num_episodes + 1):
        # monitor progress
        if i_episode % 1000 == 0:
            print("\rEpisode {}/{}.".format(i_episode, num_episodes), end="")
            sys.stdout.flush()
        # set the value of epsilon
        epsilon = 1.0 / ((i_episode / 8000) + 1)
        # generate an episode by following epsilon-greedy policy
        episode = generate_episode_from_Q(env1, env2, epsilon, nA, joueur, Q)
        # update the action-value function estimate using the episode
        update_Q_alpha(episode, alpha, gamma, Q, nA)
    # determine the policy corresponding to the final action-value function estimate
    for i in range(10):
        episode = generate_episode_from_Q(env1, env2, 0, nA, joueur, Q)
        print(episode)
    # policy1.update( dict((k,np.argmax(v)) for k, v in Q1.items()))
    if os.path.exists("./ia/ckpt/"+str(joueur)):
        file = open("./ia/ckpt/" + str(joueur), "rb")
        policy = pickle.load(file)
        file.close()
    else:
        policy = {}
    saveQ("./ia/ckpt/" + str(joueur), Q)


def train_ia(env1, env2, nb_episode, alpha):
    print("init all parameter ..")
    nA = env1.nb_square
    env1.reset()
    Q = {}
    mc_control_alpha(env1, env2, nb_episode, alpha, nA, Q, 0)

