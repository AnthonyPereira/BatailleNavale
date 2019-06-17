import os
import pickle
import random

import trainJeu



def verif(path):
    if not os.path.exists(path):
        trainJeu.train()

def check_win1(coup):
    global gagne1, gagne2 , egalite
    win=False
    if trainJeu.nbAllumette<=0:
        if(len(coup)%2==0):
            gagne2+=1
        else :
            gagne1+=1
        win=True
    elif (trainJeu.nbAllumette<min(trainJeu.coupPossible)):
        egalite+=1
        win=True
    return win

def jouer_IA(coup,j):
        """
        Parcour les tuples deja jouer et prendre le maximum pour faire jouer l'ia
        """

        coupPentiel = []
        probaCoup = j.policy[coup]
        for tupleAction, proba in probaCoup.items():
            if proba != 0:
                coupPentiel.append(tupleAction[-1])
        alleatoire = random.choice(coupPentiel)
        return coup + (alleatoire,)


gagne1=0
gagne2=0
egalite=0

cp = ""
for i in trainJeu.coupPossible:
    cp = cp + str(i) + "_"

path1 = "ia/ia1_" + str(trainJeu.name) + "_" + str(cp) + "_" + str(trainJeu.nbAllumette) + "_" + str(trainJeu.max_it) + "_" + str(trainJeu.nb_swap) + "_" + str(trainJeu.nb_train) + "_" + str(trainJeu.gamma)
path2 = "ia/ia2_" + str(trainJeu.name) + "_" + str(cp) + "_" + str(trainJeu.nbAllumette) + "_" + str(trainJeu.max_it) + "_" + str(trainJeu.nb_swap) + "_" + str(trainJeu.nb_train) + "_" + str(trainJeu.gamma)

verif(path1)
file1 = open(path1, "rb")
file2 = open(path2, "rb")
j1 = pickle.load(file1)
j2 = pickle.load(file2)
cpt=0
nbAllu=trainJeu.nbAllumette
nbPartie=100 #int(input("donner nombre de partie : "))
while nbPartie >cpt:
    coup = ()
    trainJeu.nbAllumette=nbAllu
    print("partie : ",cpt," / ",nbPartie)
    while not check_win1(coup):
        coup=jouer_IA(coup,j1)
        trainJeu.nbAllumette-=coup[-1]
        print(coup)
        if check_win1(coup):
            break
        coup = jouer_IA(coup, j2)
        trainJeu.nbAllumette -= coup[-1]
        print(coup)
    cpt+=1
print("joueur 1 a gagner : ",gagne1," fois")
print("joueur 2 a gagner : ",gagne2," fois")
print("egalite : ",egalite," fois")
