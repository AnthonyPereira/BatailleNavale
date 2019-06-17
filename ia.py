from random import randint

"""
def q_from_v(env0, env1, s, gamma=1):
    q = {}
    for next_act in env0.P[s][0]:
        q[next_act] = 0
        for next_state_that_the_enemy_take in env0.P[next_act][0]:
            probability_enemy_take_this_action = env1.policy[next_act][next_state_that_the_enemy_take]
            reward = env0.P[next_state_that_the_enemy_take][1]
            q[next_act] += probability_enemy_take_this_action * \
                           (reward + gamma * env0.V[next_state_that_the_enemy_take])
    return q
"""


def q_from_v(env0, env1, s, gamma=1):
    q = {}
    for next_act in env0.P[s][0]:
        r, f = env0.check_win(next_act)
        q[next_act] = r
        if not f:
            for next_state_that_the_enemy_take in env0.P[next_act][0]:
                probability_enemy_take_this_action = env1.policy[next_act][next_state_that_the_enemy_take]
                reward = env0.P[next_state_that_the_enemy_take][1]
                q[next_act] += probability_enemy_take_this_action * (
                            reward + gamma * env0.V[next_state_that_the_enemy_take])
    return q


def policy_improvement(env0, env1, gamma=1):
    policy = env0.get_zeros_policy()

    for s in policy.keys():

        q = q_from_v(env0, env1, s, gamma)

        #  find max

        max_val = None

        for value in q.values():
            if (max_val is None) or (value > max_val):
                max_val = value

        #  find number of max

        nb_max = 0
        for value in q.values():
            if value == max_val:
                nb_max += 1
        ######

        for key, value in q.items():
            if value == max_val:
                policy[s][key] = 1/nb_max
            else:
                policy[s][key] = 0

    env0.policy = policy


def truncated_policy_evaluation(env0, env1, max_it=1, gamma=1):
    cpt = 0
    while cpt < max_it:
        for s in env0.P.keys():
            if (len(s) % 2) == env0.player:  # -------------
                v = 0
                q = q_from_v(env0, env1, s, gamma)
                for key, value in env0.policy[s].items():
                    v += value * q[key]
                env0.V[s] = v
        cpt += 1


def truncated_policy_iteration(env0, env1, max_it=1, gamma=1, nbtry=20):

    for i in range(nbtry):
        print("train :" + str(i + 1) + "/" + str(nbtry))
        policy_improvement(env0, env1, gamma)
        truncated_policy_evaluation(env0, env1, max_it, gamma)
        print("Result : ", end="")
        print(winrate(env0, env1, 100))


def train_ia(env0, env1, nb_swap, max_it, nb_train, gamma=1):
    for i in range(nb_swap):
        print("Swap :" + str(i + 1) + "/" + str(nb_swap))
        if (i % 2) == 0:
            truncated_policy_iteration(env1, env0, max_it, gamma, nb_train)
            print(env0.policy[()])
        else:
            truncated_policy_iteration(env0, env1, max_it, gamma, nb_train)
            


def next_action(env, action):
    policy = env.policy[action]
    possible_action = []
    if len(policy) < 1:
        return None
    for i, (k, v) in enumerate(policy.items()):
        if v > 0:
            possible_action.append(k)
    nb_possible_action = len(possible_action)
    return possible_action[randint(0, nb_possible_action - 1)]


def play_a_game(env0, env1):
    turn = 0
    board = ()
    reward, final_state = env0.check_win(board)
    while not final_state:
        if (turn % 2) == 0:
            board = next_action(env0, board)
        else:
            board = next_action(env1, board)
        turn += 1
        reward, final_state = env0.check_win(board)

    return reward


def winrate(ia1, ia2, nb_game):
    if ia1.player == 0:
        env0 = ia1
        env1 = ia2
    else:
        env0 = ia2
        env1 = ia1

    kda = {"win": 0, "lose": 0, "draw": 0}
    for i in range(nb_game):
        res = play_a_game(env0, env1)
        if res == env0.WIN_VALUE:
            kda["win"] += 1
        elif res == env0.LOSS_VALUE:
            kda["lose"] += 1
        else:
            kda["draw"] += 1

    return kda
