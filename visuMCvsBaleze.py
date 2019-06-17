import time
from tkinter import *
import pickle
import ia
import iaMC2
from morpionMCenv import MorpionMCEnv

file = open("./ia/ckpt/0", "rb")
policy = pickle.load(file)
file.close()
file = open("./ia/ia2__5_5_5_1.0", "rb")
morpion_load = pickle.load(file)
file.close()


SIZE = 500
pion = 0
coup = ()
t = 2000

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

def play_game():
    nextTup = ()
    while True:
        _, reward, done = check_win(nextTup, 1)
        if done:
            if reward != MorpionMCEnv.DRAW_VALUE:
                lose += 1
            break
        if nextTup in policy:
            print(nextTup)
            action = iaMC2.nextAction(policy[nextTup], 9, nextTup)
        else:
            action = iaMC2.nextAction(nextTup, 9, nextTup)
        nextTup = nextTup + (action,)
        print()
        print(nextTup)
        _, reward, done = check_win(nextTup, 0)
        if done:
            if reward != MorpionMCEnv.DRAW_VALUE:
                win += 1
            break
        nextTup = ia.next_action(morpion_load, nextTup)
    return nextTup


def create_window(size):
    """
    create Window for playing with size
    create Window for playing with size
    """
    window = Tk()
    window.config(width=size, height=size)
    #  centrage de la fenêtre sur l'écran
    windowWidth = window.winfo_reqwidth()
    windowHeight = window.winfo_reqheight()
    positionRight = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(window.winfo_screenheight() / 2 - windowHeight / 2)
    window.geometry("+{}+{}".format(positionRight, positionDown))
    return window


def afficheParti():
    cpt = 0
    for coup in game:
        if coup == 0:
            if cpt % 2 == 0:
                btn1["text"] = "X"
            else:
                btn1["text"] = "O"

        elif coup == 1:
            if cpt % 2 == 0:
                btn2["text"] = "X"
            else:
                btn2["text"] = "O"

        elif coup == 2:
            if cpt % 2 == 0:
                btn3["text"] = "X"
            else:
                btn3["text"] = "O"

        elif coup == 3:
            if cpt % 2 == 0:
                btn4["text"] = "X"
            else:
                btn4["text"] = "O"

        elif coup == 4:
            if cpt % 2 == 0:
                btn5["text"] = "X"
            else:
                btn5["text"] = "O"

        elif coup == 5:
            if cpt % 2 == 0:
                btn6["text"] = "X"
            else:
                btn6["text"] = "O"

        elif coup == 6:
            if cpt % 2 == 0:
                btn7["text"] = "X"
            else:
                btn7["text"] = "O"

        elif coup == 7:
            if cpt % 2 == 0:
                btn8["text"] = "X"
            else:
                btn8["text"] = "O"

        elif coup == 8:
            if cpt % 2 == 0:
                btn9["text"] = "X"
            else:
                btn9["text"] = "O"
        cpt += 1
        time.sleep(2)


game = play_game()
fenetre = create_window(SIZE)
fenetre.title("Bienvenue dans le Morpion")
btn1 = Label(text=" ")
btn1.grid(column=1, row=1)
btn2 = Label(text=" ")
btn2.grid(column=2, row=1)
btn3 = Label(text=" ")
btn3.grid(column=3, row=1)
btn4 = Label(text=" ")
btn4.grid(column=1, row=2)
btn5 = Label(text=" ")
btn5.grid(column=2, row=2)
btn6 = Label(text=" ")
btn6.grid(column=3, row=2)
btn7 = Label(text=" ")
btn7.grid(column=1, row=3)
btn8 = Label(text=" ")
btn8.grid(column=2, row=3)
btn9 = Label(text=" ")
btn9.grid(column=3, row=3)
btn10 = Button(fenetre, text=" START ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'), command=afficheParti)
btn10.grid(column=2, row=4)
fenetre.mainloop()
