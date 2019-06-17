import random
from tkinter import *
from tkinter import messagebox
import pickle
import os.path
import trainJeu


TAILLEZONEBATON=500

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

def enleve_allumette(coup):
    global nbAllumette
    nbAllumette -= coup
    global canvas
    canvas.destroy()
    canvas = Canvas(fenetre, height=200, width=200, bg='white')
    canvas.pack()
    create_rec()



def verif(path):
    if not os.path.exists(path):
        trainJeu.train()

def create_rec():
    x=10
    y=10
    for i in range(nbAllumette):
        canvas.create_rectangle(x,y,x+20,y+40)
        x+=25



def enleve_allumette(coup):
    global nbAllumette
    nbAllumette-=coup
    global canvas
    canvas.destroy()
    canvas = Canvas(fenetre, height=200, width=TAILLEZONEBATON, bg='white')
    canvas.pack()
    create_rec()


def check_win1():
    if nbAllumette<=0:
        move_p0 = set()
        move_p1 = set()
        for c in range(len(coup)):
            if c % 2 == 0:
                move_p0.add(coup[c])
            else:
                move_p1.add(coup[c])
        if len(move_p0) > len(move_p1):
            if len(coup)%2 == 0:
                win("2")
            else:
                win("1")
        else:
            if len(coup)%2 == 0:
                win("1")
            else:
                win("2")
        sys.exit(0)

def check_win2():
    if nbAllumette<=0:
        move_p0 = set()
        move_p1 = set()
        for c in range(len(coup)):
            if c % 2 == 0:
                move_p0.add(coup[c])
            else:
                move_p1.add(coup[c])
        if len(move_p0) > len(move_p1):
            if len(coup)%2 == 0:
                win("1")
            else:
                win("2")
        else:
            if len(coup)%2 == 0:
                win("2")
            else:
                win("1")
        sys.exit(0)

def win(player):
    gagnant = "Bravo joueur " + player + " tu as gagné !"
    messagebox.showinfo("GG T'ES UN GENIE", gagnant)
    fenetre.destroy()

def IA1():
    #### faire le nom de fichier
    cp = ""
    for i in trainJeu.coupPossible:
        cp = cp + str(i) + "_"

    path = "ia/ia1_" + str(trainJeu.name) + "_" + str(cp) +"_" + str(trainJeu.nbAllumette) + "_" + str(trainJeu.max_it) + "_" + str(trainJeu.nb_swap) + "_" + str(trainJeu.nb_train) + "_" + str(trainJeu.gamma)

    #### verifier que le fichier existe

    def clicked1(i):
        """
        create a function when player click in the square 1
        """
        global coup
        coup = coup + (i,)
        enleve_allumette(i)
        jouer_IA()
        check_win1()

    def create_button(i):
        return Button(fenetre, text=str(i), bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=lambda: (clicked1(i)))

    def create_allCoup():
        for i in trainJeu.coupPossible:
            create_button(i).pack()

    verif(path)
    file = open(path, "rb")
    morpion_load = pickle.load(file)


    def jouer_IA():
        """
        Parcour les tuples deja jouer et prendre le maximum pour faire jouer l'ia
        """

        global coup
        coupPentiel = []
        probaCoup = morpion_load.policy[coup]
        for tupleAction, proba in probaCoup.items():
            if proba != 0:
                coupPentiel.append(tupleAction[-1])
        alleatoire = coupPentiel[random.randint(0, len(coupPentiel) - 1)]
        coup = coup + (alleatoire,)
        enleve_allumette(alleatoire)
        check_win1()

    SIZE = 500
    coup = ()
    nbAllumette=trainJeu.nbAllumette


    create_allCoup()

    canvas.pack()

    create_rec()

    jouer_IA()
    fenetre.mainloop()

def IA2():
    #### faire le nom de fichier
    cp = ""
    for i in trainJeu.coupPossible:
        cp = cp + str(i) + "_"

    path = "ia/ia2_" + str(trainJeu.name) + "_" + str(cp) + "_" + str(trainJeu.nbAllumette) + "_" + str(
        trainJeu.max_it) + "_" + str(trainJeu.nb_swap) + "_" + str(trainJeu.nb_train) + "_" + str(trainJeu.gamma)

    #### verifier que le fichier existe




    def jouer_IA():
        """
        Parcour les tuples deja jouer et prendre le maximum pour faire jouer l'ia
        """
        global coup
        coupPentiel = []
        probaCoup = morpion_load.policy[coup]
        for tupleAction, proba in probaCoup.items():
            if proba != 0:
                coupPentiel.append(tupleAction[-1])
        alleatoire = coupPentiel[random.randint(0, len(coupPentiel) - 1)]
        coup = coup + (alleatoire,)
        enleve_allumette(alleatoire)
        check_win2()

    def clicked1(i):
        """
        create a function when player click in the square 1
        """
        global coup
        coup = coup + (i,)
        enleve_allumette(i)
        jouer_IA()
        check_win2()

    def create_button(i):
        return Button(fenetre, text=str(i), bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'),
                      command=lambda: (clicked1(i)))

    def create_allCoup():
        for i in trainJeu.coupPossible:
            create_button(i).pack()

    verif(path)
    file = open(path, "rb")
    morpion_load = pickle.load(file)


    SIZE = 500
    coup = ()
    nbAllumette = trainJeu.nbAllumette


    create_allCoup()

    canvas.pack()
    create_rec()

    fenetre.mainloop()

SIZE = 500
coup = ()
nbAllumette = trainJeu.nbAllumette
fenetre=create_window(SIZE)
canvas = Canvas(fenetre, height=200, width=TAILLEZONEBATON, bg='white')

fenetre.title("Bienvenue dans Fort Boyard")

IA1()
