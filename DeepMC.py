import copy
import os
import shutil
import tensorflow as tf
import numpy as np
import time

"""
le reseaux ci-dessous doit recevoir un array d'array de 18 int
il y a 2 couches de 9 neurones a l'interieur avec comme fonction d'activation 'relu'
et une couche de 1

"""

alpha = 0.00001

def createReseaux(nbCouche=2, nbNeurone=9, nbEntre=18):
    """
    creation d'un reseau de neurone en fonction des données en entrée du nombre de neurone et le nombre de couche dans le réseau

    :param nbCouche: nombre de couche du réseau
    :param nbNeurone: nombre de neurone par couche
    :param nbEntre: nombre d'entrée
    :return: retourne la representation de l'entrée ainsi que, l'ensemble du réseau
    """
    input = tf.placeholder(tf.float32, shape=[None, nbEntre])                   # les valeurs d'entre du reseaux
    output = copy.copy(input)
    with tf.variable_scope("parametres", reuse=tf.AUTO_REUSE):                  # la sauvegarde des poids
        for i in range(0, nbCouche):                                            # nombre de couche du reseaux de neurone
            output = tf.layers.dense(output, nbNeurone, activation='relu')  # creation de la couche de neurone
        output = tf.layers.dense(output, 1)                                     # creation de la derniere couche du neurone
    return input, output


def defineFeature(state, action):
    """
    defini la feature a entree dans le reseau

    :param state: l'etat dans lequel on est
    :param action: l'action qui a été joué
    :return: le regroupement de donnée état/action qui a été jouer
    """
    feature = []
    for i in range(9):
        if i in state:                          #etat
            if state.index(i)%2 == 0:
                feature.append(1)
            else:
                feature.append(-1)
        else:
            feature.append(0)
    for i in range(9):                         #action
        if i == action:
            feature.append(1)
        else:
            feature.append(0)
    return np.array([feature])


def calculTarget(episode):
    """
    calcul le retour à avoir

    :param episode: résumé de la partie
    :return: retourne la somme des rewards de chaque etat/action de l'épisode
    """

    somme = 0
    for i in episode:
        somme += i[2]
    return [[somme]]


input, output = createReseaux()                                                 # creation du réseaux

variables = tf.trainable_variables()                                            # creation des poids
param = [var for var in variables if
         var.name.startswith("parametres")]                                     # ranger les poids qui corresponde au réseau dans un tableau


tf_target = tf.placeholder(tf.float32, shape=[None, 1], name="G_t")             # creation de la recompense additionner
gradient = tf.gradients(output, param)                                          # calcul du gradient

add = tf.add(tf_target, -output)
delta_w = []

for element in gradient:
    delta_w.append(alpha*add[0]*element)

new_param = []
for w, delta in zip(param, delta_w):
    new_param.append(w + delta)

op = []
for para1, newpara1 in zip(param, new_param):
    op.append(para1.assign(newpara1))
"""
loss = tf.losses.mean_squared_error(tf_target, output)                          # calcul de l'erreur

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.0001)             # descente de gradient avec le pas
train = optimizer.minimize(loss)                                                # fonction de minimisation de l'erreur

"""

def calculePoid(episode, joueur):
    """
    fait l'episode et tente de se rapprocher le plus possible de la valeur attendu en modifiant les poids du reseau

    :param episode: le résumé de la partie
    :param joueur: le joueur qui s'entrainé
    """

    states = []
    actions = []
    target = calculTarget(episode)
    for i in episode:
        states.append(i[0])
        actions.append(i[1])
    fichierExiste = os.path.exists("./save/"+str(joueur)+"/checkpoint")
    # saver = tf.train.Saver(param)
    if not fichierExiste:
        saver = tf.train.Saver(param)
    else:
        saver = tf.train.Saver()
    with tf.Session() as sess:
        if not fichierExiste:
            sess.run(tf.global_variables_initializer())                         # intialiser des poids
        else:
            saver.restore(sess, "./save/"+str(joueur)+"/episode.ckpt")          # recuperation des poids existant
        for i in range(len(states)):
            features = defineFeature(states[i], actions[i])
            sess.run(op, feed_dict={input: features, tf_target: target})        # entrainement du reseaux
        if fichierExiste:
            shutil.rmtree("./save/"+str(joueur))
        saver.save(sess, "./save/"+str(joueur)+"/episode.ckpt")

def foundMaximumValue(dic):
    """
    trouver la recompense la plus grande en fonction de l'action faite

    :param dic: les differente reward en fonction de l'action
    :return: la reward maximal observer
    """

    maxValue = None
    for k, v in dic.items():
        if maxValue is None or v[0][0][0] > maxValue:
            maxValue = v[0][0][0]
    return maxValue

def foundAllGoodAction(dic):
    """
    donne les actions possible

    :param dic: les differente reward en fonction de l'action
    :return: retourne toute les actions qui donne la meilleur reward
    """
    actions = []
    maxval = foundMaximumValue(dic)
    for k, v in dic.items():
        if maxval <= v[0][0][0]:
            actions.append(k)
    return actions

def nextAction(joueur, state):
    """
    defini l'action a faire en fonction des poids du réseaux

    :param joueur: le joueur qui doit jouer
    :param state: l'etat de la partie
    :return: l'action qui a été choisie
    """

    policy = {}
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, "./save/" + str(joueur) + "/episode.ckpt")
        for i in range(9):                                              # parcour toute les action
            if i not in state:                                          # defini les action possible
                features = defineFeature(state, i)
                out = sess.run([output], feed_dict={input: features})   # calcul la reward de l'action jouer
                policy[i] = out
    allGoodAction = foundAllGoodAction(policy)
    return np.random.choice(allGoodAction)


def generate_episode_from_Q(env1, env2, joueur, epsilon):
    """
    genere un episode en fonction en utilisant epsilon pour savoir si il doit explorer ou exploiter

    :param env1: l'environnement utiliser par le joueur 0
    :param env2: l'environnement utiliser par le joueur 1
    :param joueur: le joueur qui s'entraine
    :param epsilon: la variable permettant de savoir si le joueur s'entrainant doit explorer ou exploiter

    """
    episode = []
    state = env1.reset()
    cpt = 0
    fichierExiste1 = os.path.exists("./save/" + str(joueur)+"/checkpoint")
    if joueur == 0:
        fichierExiste2 = os.path.exists("./save/1/checkpoint")
    else:
        fichierExiste2 = os.path.exists("./save/0/checkpoint")
    while True:
        if cpt % 2 == joueur:                                                                               #joueur a entrainer
            if fichierExiste1:                                                                                     # si les poids existe choisir entre exporation ou exploitation
                action = (env1.getRandom() if np.random.random() < epsilon else nextAction(joueur, state))
            else:                                                                                                  # sinon exploration
                action = env1.getRandom(state)
            next_state, reward, done = env1.check_win(state + (action,))
            if joueur == 0:
                episode.append((state, action, reward))                                                            # sauvegarde pour resumé de partie
        else:                                                                                               # joueur qui entraine l'autre
            if fichierExiste2:                                                                                     # si les poids de l'IA qui entraine l'autre existe alors exploitation
                if joueur == 0:
                    action = nextAction(1, state)
                else:
                    action = nextAction(0, state)
            else:                                                                                                   # sinon IA random
                action = env2.getRandom(state)
            next_state, reward, done = env2.check_win(state + (action,))
        env1.step(action)
        env1.nb_square -= 1
        env2.nb_square -= 1
        cpt += 1
        state = next_state
        if done:
            if joueur == cpt:                                                                                       # si c'est le joueur qui entraine qui a fini alors donner la reward inverse au joueur qui s'entraine
                episode[len(episode)-1] = (state[:len(state)-2], state[len(state)-2], -reward)
            print(episode)
            break
    env1.reset()
    env2.reset()
    return episode


def mc_control_alpha(env1, env2, num_episodes, joueur):
    """
    fait un certains nombres d'épisodes et modifie les poids a chaque episode

    :param env1: l'environnement utiliser par le joueur 0
    :param env2: l'environnement utiliser par le joueur 1
    :param num_episodes: le nombre de partie jouer
    :param joueur: le joueur qui s'entraine
    """
    # loop over episodes
    sommeTempsPartie = 0
    sommeTempsCalculPoid = 0
    epsilon = 1
    for i_episode in range(0, num_episodes):
        debutPartie = time.time()
        # monitor progress
        if i_episode%10 == 0: 
            print(i_episode)
        # set the value of epsilon
        if epsilon > 0.1:
            epsilon = 1.0 / ((i_episode / 8) + 1)
        # generate an episode by following epsilon-greedy policy
        episode = generate_episode_from_Q(env1, env2, joueur, epsilon)
        # update the action-value function estimate using the episode
        finPartie = time.time()
        debutCalculPoid = time.time()
        calculePoid(episode, joueur)
        finCalculPoid = time.time()
        sommeTempsPartie += finPartie-debutPartie
        sommeTempsCalculPoid += finCalculPoid-debutCalculPoid
    print("la moyenne des temps de parties est de :"+ str(sommeTempsPartie/num_episodes) + " et le calcul des poids a duré : " + str(sommeTempsCalculPoid/num_episodes))


def train_ia(env1, env2, nb_swap, nb_episode):
    """
    permet "d'entrainer" les 2 IA l'une contre l'autre

    :param env1: l'environnement utiliser par le joueur 0
    :param env2: l'environnement utiliser par le joueur 1
    :param nb_swap: le nombre de fois ou l'IA 1 et IA 2 se change entre elles pour s'entrainer l'une contre l'autre
    :param nb_episode: le nombre de partie dans un swap
    """
    print(tf.test.gpu_device_name())
    for i in range(0, nb_swap):
        debut = time.time()
        print("swap : ", i + 1, "/", nb_swap)
        print()
        if i % 2 == 0:
            mc_control_alpha(env1, env2, nb_episode, 0)
        else:
            mc_control_alpha(env2, env1, nb_episode, 1)
        print()
        fin = time.time()
        print("le swap a duré : "+str(fin-debut))
