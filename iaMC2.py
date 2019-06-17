import sys
import time

import numpy as np
import pickle


def saveQ(file_name, Q):
    """
    sauvegarde Q dans un fichier

    :param file_name: chemin + nom du fichier ou sauvegarder
    :param Q: l'objet à sauvegarder
    """
    file = open(file_name, "wb")
    pickle.dump(Q, file)
    file.close()


def nextAction(Q, nA, state):
    """
    choix de la prochaine action en fonction de l'état

    :param Q: la " politique ", ou plutot la moyenne des rewards en fonction de l'etat
    :param nA: le nombre d'action total du jeu
    :param state: l'etat du jeu
    :return: l'action qui va etre jouer
    """
    strat = []
    if type(Q) is tuple:
        for i in range(nA):
            if i not in Q:
                strat.append(1/(nA-len(Q)))
            else:
                strat.append(0)
    else:
        strat = get_probs(state, Q, 0, nA)
    return np.random.choice(np.arange(nA), p=strat)


def max(state, Q_s, nA):
    """
    trouve l'action sur laquel la reward est la plus élevé

    :param state: etat dans lequel le jeu est
    :param Q_s: toute les reward des actions dans cette etat
    :param nA: toute les actions possible du jeu
    :return: l'action avec la meilleur reward
    """
    maxValue = None
    maxAction = None
    for i in range(0, nA):
        if i not in state and (maxValue is None or maxValue < Q_s[i]):
            maxValue = Q_s[i]
            maxAction = i
    return maxAction


def get_probs(state, Q_s, epsilon, nA):
    """
    permet d'obtenir la probabilité de jouer cette action en fonction des moyennes des rewards obtenu et en fonction d'epsilon

    :param state: l'etat dans lequel on est
    :param Q_s: les moyennes des reward obtenu sur chaque action jouer dans cette etat
    :param epsilon: décide si l'on doit plus privilégier l'exploitation des résultat obtenue ou l'exploration
    :param nA: le nombre d'action total de l'environnement
    """
    policy_s = np.ones(nA) * epsilon / (nA - len(state))
    best_a = max(state, Q_s, nA)
    policy_s[best_a] = 1 - epsilon + (epsilon / (nA - len(state)))
    for i in range(nA):
        if i in state:
            policy_s[i] = 0
    return policy_s


def generate_episode_from_Q(env1, env2, epsilon, nA, joueur, Q1, Q2):
    """
    genere un episode en fonction de la probabilité calculer de jouer les actions

    :param env1: l'environnement de l'IA 1
    :param env2: l'environnement de l'IA 2
    :param epsilon: décide si l'on doit plus privilégier l'exploitation des résultat obtenue ou l'exploration
    :param nA: le nombre d'action total de l'environnement
    :param joueur: le numero de l'IA qui s'entraine
    :param Q1: la " politique ", ou plutot la moyenne des rewards en fonction de l'etat de l'IA 1
    :param Q2: la " politique ", ou plutot la moyenne des rewards en fonction de l'etat de l'IA 2
    """
    episode = []
    state = env1.reset()
    cpt = 0
    while True:
        if cpt % 2 == joueur:
            action = np.random.choice(np.arange(nA),
                                      p=get_probs(state, Q1[state], epsilon, nA)) if state in Q1 else env1.getRandom(state)
            next_state, reward, done = env1.check_win(state + (action,))
        else:
            action = np.random.choice(np.arange(nA),
                                      p=get_probs(state, Q2[state], 0, nA)) if state in Q2 else env2.getRandom(state)
            next_state, reward, done = env2.check_win(state + (action,))
        if joueur == cpt % 2:
            episode.append((state, action, reward))
        env1.step(action)
        env1.nb_square -= 1
        env2.nb_square -= 1
        cpt += 1
        state = next_state
        if done:
            if joueur == cpt % 2:
                if reward == 100:
                    episode[len(episode)-1] = (state[:len(state)-2], state[len(state)-2], -reward)
            break
    env1.reset()
    env2.reset()
    return episode


def update_Q_alpha(episode, alpha, gamma, Q, nA):
    """
    met a jour Q avec les nouvelle reward obtenu pendant la derniere partie

    :param episode: resumer de la partie jouer
    :param alpha: permet que chaque episode est le meme poids sur l'apprentissage de l'IA
    :param gamma: jusqu'ou on pousse les recherche dans les rewards futur
    :param Q: la " politique ", ou plutot la moyenne des rewards en fonction de l'etat a mettre a jour
    :param nA: le nombre d'action total de l'environnement
     """
    states, actions, rewards = zip(*episode)
    # prepare for discounting
    discounts = np.array([gamma ** i for i in range(len(rewards) + 1)])
    for i, state in enumerate(states):

        if state not in Q:
            Q[state] = np.zeros(nA)
            old_Q = Q[state][actions[i]]
        else:
            old_Q = Q[state][actions[i]]
        Q[state][actions[i]] = old_Q + alpha * (sum(rewards[i:] * discounts[:-(1 + i)]) - old_Q)


def mc_control_alpha(env1, env2, num_episodes, alpha, nA, Q1, Q2, joueur, gamma=1.0):
    """
     fait l'entrainement du swap

    :param env1: l'environnement de l'IA 1
    :param env2: l'environnement de l'IA 2
    :param num_episodes: nombre de partie a faire
    :param alpha: permet que chaque episode est le meme poids sur l'apprentissage de l'IA
    :param nA: le nombre d'action total de l'environnement
    :param Q1: la " politique ", ou plutot la moyenne des rewards en fonction de l'etat de l'IA 1
    :param Q2: la " politique ", ou plutot la moyenne des rewards en fonction de l'etat de l'IA 2
    :param joueur: le joueur a entrainer
    :param gamma: la profondeur a laquelle on va aller pour les reward futur
    """

    # loop over episodes
    epsilon = 1
    for i_episode in range(1, num_episodes + 1):

        # monitor progress
        if i_episode % 1000 == 0:
            print("\rEpisode {}/{}.".format(i_episode, num_episodes), end="")
            sys.stdout.flush()
        # set the value of epsilon
        if epsilon > 0.1:
            epsilon = 1.0 / ((i_episode / 8000) + 1)
        # generate an episode by following epsilon-greedy policy
        episode = generate_episode_from_Q(env1, env2, epsilon, nA, joueur, Q1, Q2)
        # update the action-value function estimate using the episode
        update_Q_alpha(episode, alpha, gamma, Q1, nA)
    # determine the policy corresponding to the final action-value function estimate

    # policy1.update( dict((k,np.argmax(v)) for k, v in Q1.items()))

    saveQ("./ia/ckpt/" + str(joueur), Q1)


def train_ia(env1, env2, nb_swap, nb_episode, alpha):
    print("init all parameter ..")
    nA = env1.nb_square
    env1.nb_square -= 1
    env2.nb_square -= 1
    env1.reset()
    env2.reset()
    Q1 = {}
    Q2 = {}
    for i in range(0, nb_swap):
        debut = time.time()
        print("swap : ", i + 1, "/", nb_swap)
        print()
        if i % 2 == 0:
            mc_control_alpha(env1, env2, nb_episode, alpha, nA, Q1, Q2, 0)
        else:
            mc_control_alpha(env2, env1, nb_episode, alpha, nA, Q2, Q1, 1)
        fin = time.time()
        print("le swap a durer : " + str(fin-debut))
        print()
