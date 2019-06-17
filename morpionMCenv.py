import copy
import pickle
import numpy as np

move_list = ()      # etat ou ensemble des action joué


def setMoveList(state):
    """
    change les action joué

    :param state: nouvelle série d'action jouer
    """
    global move_list
    move_list = state


class MorpionMCEnv():
    WIN_VALUE = 100         # reward gagné
    DRAW_VALUE = 20          # reward egalité
    SAME_VALUE = -1000      # reward déjà joué
    LOSS_VALUE = -100       # reward perdu

    def __init__(self, player, size=3):

        self.nb_square = size * size    # nombre de case
        self.player = player            # joueur de l'environnement
        self.size = size                # taille d'une ligne ou d'une colonne du plateau
        self.cpt = 0

    def dejaJouer(self, coup, state):
        return coup in state

    def check_win(self, move=copy.copy(move_list), player=None):

        """ Check is the current state is a winning stage

        :param player: le joueur a qui on test la win
        :param move: état dans lequel le plateau est
        :return: état dans lequel le plateau est, la reward, si la partie est finie ou pas
        """

        if player is None:
            player = self.player

        move_p0 = set()
        move_p1 = set()

        last_move_p0 = None
        for c in range(len(move)):              # defini les coup jouer par les differents joueur
            if c % 2 == 0:                              #joueur 1
                if c < len(move)-1:
                    move_p0.add(move[c])
                else:
                    last_move_p0 = move[c]
            else:                                       #joueur 2
                move_p1.add(move[c])

        winning_states = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},       # initialise les cas de win
                          {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]


        for i in range(2):
            for w_state in winning_states:
                if move_p0.issuperset(w_state):                         # verifie si le joueur 1 a gagner
                    if player == 0:
                        return move, MorpionMCEnv.WIN_VALUE, True
                    else:
                        return move, MorpionMCEnv.LOSS_VALUE, True

                if move_p1.issuperset(w_state):

                    if player == 1:                                     # verifie si le joueur 2 a gagner
                        return move, MorpionMCEnv.WIN_VALUE, True
                    else:
                        return move, MorpionMCEnv.LOSS_VALUE, True
            move_p0.add(last_move_p0)

        if len(move) == self.size * self.size:                      # verifie si c'est une égalité
            return move, MorpionMCEnv.DRAW_VALUE, True

        return move, MorpionMCEnv.DRAW_VALUE, False                 # retourne si la partie n'est pas terminée

    def reset(self):
        """
        reset l'etat du plateau

        :return: état du plateau
        """
        global move_list
        move_list = ()
        self.nb_square = self.size * self.size
        return move_list

    def step(self, move):
        """
        ajoute l'action a toute les action de la partie

        :param move: action joué
        """

        global move_list
        move_list = move_list + (move,)

    def getMove_list(self):
        """
        prendre toute les actions jouer (etat du plateau)

        :return: etat du plateau
        """
        return move_list

    def getRandom(self, state=move_list):
        """
        donne une action random qui sera jouer

        :param state: toutes les action deja jouer
        :return: une action a jouer
        """
        liste = []
        for i in range(0, self.size * self.size):
            if i not in state:
                liste.append(i)
        return np.random.choice(liste)

    def save_env(self, file_name, policy):
        file = open(file_name, "wb")
        pickle.dump(policy, file)
