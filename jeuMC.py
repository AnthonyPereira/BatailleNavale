from tkinter import *
from tkinter import messagebox
import pickle
import iaMC2

SIZE = 500
pion = 0
coup = ()

def stopper():
    demandeF.destroy()


def rejouer():
    demandeF.destroy()
    root = Tk()
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
    root.geometry("+{}+{}".format(positionRight, positionDown))
    label = Label(root, text="Contre qui voulez-vous jouer ?")
    label.pack()
    go1 = Button(root, text="IA1", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'), command=ChoixJ1)
    go1.pack()
    go2 = Button(root, text="IA2", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'), command=ChoixJ2)
    go2.pack()
    root.mainloop()

def demande():
    global demandeF
    demandeF = Tk()
    windowWidth = demandeF.winfo_reqwidth()
    windowHeight = demandeF.winfo_reqheight()
    positionRight = int(demandeF.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(demandeF.winfo_screenheight() / 2 - windowHeight / 2)
    demandeF.geometry("+{}+{}".format(positionRight, positionDown))
    continuer = Button(demandeF, text="Joueur1", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                       command=rejouer)
    continuer.pack()
    arreter = Button(demandeF, text="", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                     command=stopper())
    arreter.pack()
    root.mainloop()

def ChoixJ1():
    root.destroy()

    pion = 0
    coup = ()

    file = open("./ia/ckpt/0", "rb")
    morpion_load = pickle.load(file)




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

    def clicked1():
        """
        create a function when player click in the square 1
        """
        global coup
        coup = coup + (0,)
        if btn1["text"] == " ":
            btn1["text"] = "O"
        jouer_IA()
        check_win()

    def clicked2():
        """
        create a function when player click in the square 2
        """
        global coup
        coup = coup + (1,)
        if btn2["text"] == " ":
            btn2["text"] = "O"
        jouer_IA()
        check_win()

    def clicked3():
        """
        create a function when player click in the square 3
        """
        global coup
        coup = coup + (2,)
        if btn3["text"] == " ":
            btn3["text"] = "O"
        jouer_IA()
        check_win()

    def clicked4():
        """
        create a function when player click in the square 4
        """
        global coup
        coup = coup + (3,)
        if btn4["text"] == " ":
            btn4["text"] = "O"
        jouer_IA()
        check_win()

    def clicked5():
        """
        create a function when player click in the square 5
        """
        global coup
        coup = coup + (4,)
        if btn5["text"] == " ":
            btn5["text"] = "O"
        jouer_IA()
        check_win()

    def clicked6():
        """
        create a function when player click in the square 6
        """
        global coup
        coup = coup + (5,)
        if btn6["text"] == " ":
            btn6["text"] = "O"
        jouer_IA()
        check_win()

    def clicked7():
        """
        create a function when player click in the square 7
        """
        global coup
        coup = coup + (6,)
        if btn7["text"] == " ":
            btn7["text"] = "O"
        jouer_IA()
        check_win()

    def clicked8():
        """
        create a function when player click in the square 8
        """
        global coup
        coup = coup + (7,)
        if btn8["text"] == " ":
            btn8["text"] = "O"
        jouer_IA()
        check_win()

    def clicked9():
        """
        create a function when player click in the square 9
        """
        global coup
        coup = coup + (8,)
        if btn9["text"] == " ":
            btn9["text"] = "O"
        jouer_IA()
        check_win()

    def jouer_IA():
        """
        Parcour les tuples deja jouer et prendre le maximum pour faire jouer l'ia
        """
        global coup
        if coup in morpion_load:
            print(coup)
            action = iaMC2.nextAction(morpion_load[coup], 9, coup)
        else:
            action = iaMC2.nextAction(coup, 9, coup)
        coup = coup + (action,)
        if action == 0:
            btn1["text"] = "X"

        elif action == 1:
            btn2["text"] = "X"

        elif action == 2:
            btn3["text"] = "X"

        elif action == 3:
            btn4["text"] = "X"

        elif action == 4:
            btn5["text"] = "X"

        elif action == 5:
            btn6["text"] = "X"

        elif action == 6:
            btn7["text"] = "X"

        elif action == 7:
            btn8["text"] = "X"

        elif action == 8:
            btn9["text"] = "X"
        check_win()

    def check_win():
        global pion
        b1 = btn1["text"]
        b2 = btn2["text"]
        b3 = btn3["text"]
        b4 = btn4["text"]
        b5 = btn5["text"]
        b6 = btn6["text"]
        b7 = btn7["text"]
        b8 = btn8["text"]
        b9 = btn9["text"]
        pion += 1
        if b1 == b2 and b1 == b3 and b1 == "O" or b1 == b2 and b1 == b3 and b1 == "X":  # LIGNE 1
            win(btn1["text"])
        elif b4 == b5 and b4 == b6 and b4 == "O" or b4 == b5 and b4 == b6 and b4 == "X":  # LIGNE 2
            win(btn4["text"])
        elif b7 == b8 and b7 == b9 and b7 == "O" or b7 == b8 and b7 == b9 and b7 == "X":  # LIGNE 3
            win(btn7["text"])
        elif b1 == b4 and b1 == b7 and b1 == "O" or b1 == b4 and b1 == b7 and b1 == "X":  # COLONNE 1
            win(btn1["text"])
        elif b2 == b5 and b2 == b8 and b2 == "O" or b2 == b5 and b2 == b8 and b2 == "X":  # COLONNE 2
            win(btn2["text"])
        elif b3 == b6 and b3 == b9 and b3 == "O" or b3 == b6 and b3 == b9 and b3 == "X":  # COLONNE 3
            win(btn3["text"])
        elif b1 == b5 and b1 == b9 and b1 == "O" or b1 == b5 and b1 == b9 and b1 == "X":  # DIAGONALE 1
            win(btn1["text"])
        elif b3 == b5 and b3 == b7 and b3 == "O" or b3 == b5 and b3 == b7 and b3 == "X":  # DIAGONALE 2
            win(btn3["text"])
        elif pion == 9:
            fenetre.destroy()
            demande()

    def win(player):
        gagnant = "Bravo " + player + " tu as gagné !"
        messagebox.showinfo("GG T'ES UN GENIE", gagnant)
        fenetre.destroy()
        demande()


    fenetre = create_window(SIZE)
    fenetre.title("Bienvenue dans le Morpion")
    btn1 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                  command=clicked1)
    btn1.grid(column=1, row=1)
    btn2 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                  command=clicked2)
    btn2.grid(column=2, row=1)
    btn3 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked3)
    btn3.grid(column=3, row=1)
    btn4 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked4)
    btn4.grid(column=1, row=2)
    btn5 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked5)
    btn5.grid(column=2, row=2)
    btn6 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked6)
    btn6.grid(column=3, row=2)
    btn7 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked7)
    btn7.grid(column=1, row=3)
    btn8 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked8)
    btn8.grid(column=2, row=3)
    btn9 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                 command=clicked9)
    btn9.grid(column=3, row=3)
    jouer_IA()
    fenetre.mainloop()

def ChoixJ2():
    root.destroy()

    pion = 0
    coup = ()

    file = open("./ia/ia2__5_5_5_1.0", "rb")
    morpion_load = pickle.load(file)


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

    def clicked1():
        """
        create a function when player click in the square 1
        """
        global coup
        coup = coup + (0,)
        if btn1["text"] == " ":
            btn1["text"] = "O"
        check_win()
        jouer_IA()

    def clicked2():
        """
        create a function when player click in the square 2
        """
        global coup
        coup = coup + (1,)
        if btn2["text"] == " ":
            btn2["text"] = "O"
        check_win()
        jouer_IA()

    def clicked3():
        """
        create a function when player click in the square 3
        """
        global coup
        coup = coup + (2,)
        if btn3["text"] == " ":
            btn3["text"] = "O"
        check_win()
        jouer_IA()

    def clicked4():
        """
        create a function when player click in the square 4
        """
        global coup
        coup = coup + (3,)
        if btn4["text"] == " ":
            btn4["text"] = "O"
        check_win()
        jouer_IA()

    def clicked5():
        """
        create a function when player click in the square 5
        """
        global coup
        coup = coup + (4,)
        if btn5["text"] == " ":
            btn5["text"] = "O"
        check_win()
        jouer_IA()

    def clicked6():
        """
        create a function when player click in the square 6
        """
        global coup
        coup = coup + (5,)
        if btn6["text"] == " ":
            btn6["text"] = "O"
        check_win()
        jouer_IA()

    def clicked7():
        """
        create a function when player click in the square 7
        """
        global coup
        coup = coup + (6,)
        if btn7["text"] == " ":
            btn7["text"] = "O"
        check_win()
        jouer_IA()

    def clicked8():
        """
        create a function when player click in the square 8
        """
        global coup
        coup = coup + (7,)
        if btn8["text"] == " ":
            btn8["text"] = "O"
        check_win()
        jouer_IA()

    def clicked9():
        """
        create a function when player click in the square 9
        """
        global coup
        coup = coup + (8,)
        if btn9["text"] == " ":
            btn9["text"] = "O"
        check_win()
        jouer_IA()

    def jouer_IA():
        """
        Parcour les tuples deja jouer et prendre le maximum pour faire jouer l'ia
        """
        global coup
        if coup in morpion_load:
            print(coup)
            action = iaMC2.nextAction(morpion_load[coup], 9, coup)
        else:
            action = iaMC2.nextAction(coup, 9, coup)
        coup = coup + (action,)
        if action == 0:
            btn1["text"] = "X"

        elif action == 1:
            btn2["text"] = "X"

        elif action == 2:
            btn3["text"] = "X"

        elif action == 3:
            btn4["text"] = "X"

        elif action == 4:
            btn5["text"] = "X"

        elif action == 5:
            btn6["text"] = "X"

        elif action == 6:
            btn7["text"] = "X"

        elif action == 7:
            btn8["text"] = "X"

        elif action == 8:
            btn9["text"] = "X"
        check_win()

    def check_win():
        global pion
        b1 = btn1["text"]
        b2 = btn2["text"]
        b3 = btn3["text"]
        b4 = btn4["text"]
        b5 = btn5["text"]
        b6 = btn6["text"]
        b7 = btn7["text"]
        b8 = btn8["text"]
        b9 = btn9["text"]
        pion += 1
        if b1 == b2 and b1 == b3 and b1 == "O" or b1 == b2 and b1 == b3 and b1 == "X":  # LIGNE 1
            win(btn1["text"])
        elif b4 == b5 and b4 == b6 and b4 == "O" or b4 == b5 and b4 == b6 and b4 == "X":  # LIGNE 2
            win(btn4["text"])
        elif b7 == b8 and b7 == b9 and b7 == "O" or b7 == b8 and b7 == b9 and b7 == "X":  # LIGNE 3
            win(btn7["text"])
        elif b1 == b4 and b1 == b7 and b1 == "O" or b1 == b4 and b1 == b7 and b1 == "X":  # COLONNE 1
            win(btn1["text"])
        elif b2 == b5 and b2 == b8 and b2 == "O" or b2 == b5 and b2 == b8 and b2 == "X":  # COLONNE 2
            win(btn2["text"])
        elif b3 == b6 and b3 == b9 and b3 == "O" or b3 == b6 and b3 == b9 and b3 == "X":  # COLONNE 3
            win(btn3["text"])
        elif b1 == b5 and b1 == b9 and b1 == "O" or b1 == b5 and b1 == b9 and b1 == "X":  # DIAGONALE 1
            win(btn1["text"])
        elif b3 == b5 and b3 == b7 and b3 == "O" or b3 == b5 and b3 == b7 and b3 == "X":  # DIAGONALE 2
            win(btn3["text"])
        elif len(coup) == 9:
            fenetre.destroy()
            demande()

    def win(player):
        gagnant = "Bravo " + player + " tu as gagné !"
        messagebox.showinfo("GG T'ES UN GENIE", gagnant)
        fenetre.destroy()
        demande()

    if __name__ == '__main__':
        fenetre = create_window(SIZE)
        fenetre.title("Bienvenue dans le Morpion")
        btn1 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked1)
        btn1.grid(column=1, row=1)
        btn2 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked2)
        btn2.grid(column=2, row=1)
        btn3 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked3)
        btn3.grid(column=3, row=1)
        btn4 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked4)
        btn4.grid(column=1, row=2)
        btn5 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked5)
        btn5.grid(column=2, row=2)
        btn6 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked6)
        btn6.grid(column=3, row=2)
        btn7 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked7)
        btn7.grid(column=1, row=3)
        btn8 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked8)
        btn8.grid(column=2, row=3)
        btn9 = Button(fenetre, text=" ", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=clicked9)
        btn9.grid(column=3, row=3)
        fenetre.mainloop()



root = Tk()
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
root.geometry("+{}+{}".format(positionRight, positionDown))
label = Label(root,text="Contre qui voulez-vous jouer ?")
label.pack()
go1= Button(root, text="IA1", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'), command=ChoixJ1)
go1.pack()
go2= Button(root, text="IA2", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'), command=ChoixJ2)
go2.pack()
root.mainloop()