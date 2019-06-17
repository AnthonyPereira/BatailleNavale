import copy
import pickle


class MorpionEnv:
    """Morpion env"""

    WIN_VALUE = 100
    LOSS_VALUE = -100
    DRAW_VALUE = 0

    def __init__(self, grid_size, player):
        """Create a Morpion env


        :param grid_size:
        :param player: (0 or 1)
        """

        if player != 1 and player != 0:
            print("Player value incorrect")

        self.player = player
        self.grid_size = grid_size
        self.nb_square = grid_size*grid_size
        self.P = {}
        self.policy = {}
        self.V = {}

    def generate_random_policy(self):
        for key, value in self.P.items():
            if (len(key) % 2) == self.player:  # -------------
                self.policy[key] = {}
                number_of_next_state = len(value[0])
                for next_state in value[0]:
                    self.policy[key][next_state] = 1 / number_of_next_state

    def get_zeros_policy(self):
        policy = {}
        for key, value in self.P.items():
            if (len(key) % 2) == self.player:  # -------------
                policy[key] = {}
                for next_state in value[0]:
                    policy[key][next_state] = 0
        return policy

    def generate_v(self):
        for key in self.P.keys():
            if (len(key) % 2) == self.player:  # -------------
                self.V[key] = 0

    def check_win(self, move_list):
        """ Check is the current state is a winning stage

        :param move_list:
        :return reward, is it a final state
        """

        move_p0 = set()
        move_p1 = set()

        for c in range(len(move_list)):
            if c % 2 == 0:
                move_p0.add(move_list[c])
            else:
                move_p1.add(move_list[c])

        winning_states = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},
                          {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]

        for w_state in winning_states:

            if move_p0.issuperset(w_state):
                if self.player == 0:
                    return MorpionEnv.WIN_VALUE, True
                else:
                    return MorpionEnv.LOSS_VALUE, True

            if move_p1.issuperset(w_state):
                if self.player == 1:
                    return MorpionEnv.WIN_VALUE, True
                else:
                    return MorpionEnv.LOSS_VALUE, True

        if len(move_list) == self.nb_square:
            return MorpionEnv.DRAW_VALUE, True

        return MorpionEnv.DRAW_VALUE, False

    def rec_generate_p(self, move_list):
        """Initialize P
        :param move_list
        :return nothing:
        """
        reward, final_state = self.check_win(move_list)
        self.P[move_list] = [[], reward, final_state]
        if len(move_list) == self.nb_square:
            return

        if final_state:  # -------------
            return  #-------------

        for move in range(self.nb_square):
            if move not in move_list:
                new_list = copy.copy(move_list)
                new_list = new_list+(move,)
                self.P[move_list][0].append(new_list)
                self.rec_generate_p(new_list)

    def generate_p(self):
        self.rec_generate_p(())

    def save_p(self, file_name):
        file = open(file_name, "wb")
        pickle.dump(self.P, file)

    def load_p(self, file_name):
        file = open(file_name, "rb")
        self.P = pickle.load(file)

    def save_policy(self, file_name):
        file = open(file_name, "wb")
        pickle.dump(self, file)

    def load_policy(self, file_name):
        file = open(file_name, "rb")
        self.policy = pickle.load(self, file)

    def save_env(self, file_name):
        file = open(file_name, "wb")
        pickle.dump(self, file)




