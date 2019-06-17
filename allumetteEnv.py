import copy
import pickle


class AllumetteEnv:
    """Morpion env"""

    WIN_VALUE = 10000
    LOSS_VALUE = -10000
    DRAW_VALUE = -100

    def __init__(self, nbAllumette, player, coupPossible):
        """Create a Morpion env


        :param grid_size:
        :param player: (0 or 1)
        """

        if player != 1 and player != 0:
            print("Player value incorrect")

        self.player = player
        self.nbAllumette = nbAllumette
        self.coupPossible = coupPossible
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
        """ regarde si la partie est gagné

        :param move_list: les actions qui ont été jouer
        :return reward, et si la partie est fini
        """


        AllumetteEnleve=0
        for c in move_list:
            AllumetteEnleve += c


        if AllumetteEnleve==self.nbAllumette:
            if len(move_list)%2==0:
                if self.player==0 :
                    return AllumetteEnv.WIN_VALUE , True
                else :
                    return AllumetteEnv.LOSS_VALUE , True
            else :
                if self.player==0 :
                    return AllumetteEnv.LOSS_VALUE , True
                else :
                    return AllumetteEnv.WIN_VALUE , True
        if self.nbAllumette-AllumetteEnleve<min(self.coupPossible):
            return AllumetteEnv.DRAW_VALUE,True

        return AllumetteEnv.DRAW_VALUE,False

    def rec_generate_p(self, move_list ,resteAllumette,i=0):
        """Initialize P
        :param move_list
        :return nothing:
        """

        reward, final_state = self.check_win(move_list)
        self.P[move_list] = [[], reward, final_state]
        if resteAllumette<min(self.coupPossible):
            if i==0:
                new_list = copy.copy(move_list)
                new_list = new_list #+ (0,)
                self.P[move_list][0].append(new_list)
                self.rec_generate_p(new_list, resteAllumette,1)  #-------------
            else :
                return

        if resteAllumette==0:
            if i==0:
                new_list = copy.copy(move_list)
                new_list = new_list #+ (0,)
                self.P[move_list][0].append(new_list)
                self.rec_generate_p(new_list, resteAllumette,1)  #-------------
            else :
                return

        if final_state:  # -------------
            if i==0:
                new_list = copy.copy(move_list)
                new_list = new_list #+ (0,)
                self.P[move_list][0].append(new_list)
                self.rec_generate_p(new_list, resteAllumette,1)  #-------------
            else :
                return

        for move in (self.coupPossible):
            if resteAllumette-move >= 0 :
                new_list = copy.copy(move_list)
                new_list = new_list+(move,)
                self.P[move_list][0].append(new_list)
                self.rec_generate_p(new_list,resteAllumette-move)

    def generate_p(self):
        self.rec_generate_p((), self.nbAllumette)

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




