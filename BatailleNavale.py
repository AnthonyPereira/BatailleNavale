#### Pereira Anthony    #### Pierson Quentin   ####
from random import *
import os 

def initialiser_grille():
	"""
	initialise un tableau de 10x10 avec des -1
	:return:tableau générer
	:rtype:list
	
	>>> initialiser_grille()
	[[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]
	
	"""
	grille=[]
	for i in range(10):
		grille.append([])
		for j in range(10):
			grille[i].append(-1)
	return grille

def verif(grille:list,sens:int,varBateaux:int,notVarBateaux:int,tailleBateaux:int):
		"""
		verifie si le un bateaux donné peut se positionner
		:param grille: le tableau avec des bateux positionner dessus
		:param sens: le sens du bateau
		:param varBateaux: longueur du bateaux
		:param notVarBateaux:largeur du bateaux
		:param tailleBateaux:la taille du bateaux
		:type grille: list
		:type sens: int
		:type varBateaux: int
		:type notVarBateaux:int
		:type tailleBateaux:int
		:return: si le bateaux peut etre placer ou pas
		:rtype: bool
		"""		
		if sens == 0:
			for i in range(tailleBateaux):
				if grille[notVarBateaux][varBateaux]!=-1:
					return False
				if varBateaux!=0:
					if grille[notVarBateaux][varBateaux-1]!=-1:
						return False
				if notVarBateaux!=0:	
					if grille[notVarBateaux-1][varBateaux]!=-1:
						return False
				if notVarBateaux!=9:
					if grille[notVarBateaux+1][varBateaux]!=-1:
						return False
				if varBateaux!=9:	
					if grille[notVarBateaux][varBateaux+1]!=-1:
						return False
				varBateaux+=1
			return True
			
		if sens == 1:
			for i in range(tailleBateaux):
				if grille[varBateaux][notVarBateaux]!=-1:
					return False
				if notVarBateaux!=0:	
					if grille[varBateaux][notVarBateaux-1]!=-1:
						return False
				if varBateaux!=0:
					if grille[varBateaux-1][notVarBateaux]!=-1:
						return False
				if varBateaux!=9:
					if grille[varBateaux+1][notVarBateaux]!=-1:
						return False
				if notVarBateaux!=9:
					if grille[varBateaux][notVarBateaux+1]!=-1:
						return False
				varBateaux+=1
			return True

def placer_bateaux(grille:list):
	"""
	place les bateaux aléatoirement sur un tableau
	:param grille: le tableau ou il faut placer les bateaux
	:type grille: list
	:return: la grille avec les bateaux dedans
	:rtype: list
	
	"""
	bateaux={"porte_avion":[3,3,3,3,3],"croiseur":[4,4,4,4],"contre_torpilleur":[5,5,5],"sous_marin":[6,6,6],"torpilleur":[7,7]}

	

	
	
	for i in bateaux:
		longueurBateaux=len(bateaux[i])
		y=1
		sens=randint(0,1)
		positionX=randint(1,len(bateaux[i]))
		positionY=randint(1,9)
		
		while verif(grille,sens,positionX,positionY,longueurBateaux)==False:
			sens=randint(0,1)
			positionX=randint(1,len(bateaux[i]))
			positionY=randint(1,9)
		if sens == 0:
			for j in range(longueurBateaux):
				grille[positionY][positionX]=bateaux[i][j]
				
				positionX+=1

			
		if sens == 1:
			for j in range(longueurBateaux):
				grille[positionX][positionY]=bateaux[i][j]
				positionX+=1
	return(grille)	

				

	
def tir_valide(tirs:list,ligne:int,colonne:int):
	"""
	verifie si le tir est valide
	:param tirs: le tableau avec les tirs effectuer
	:param ligne:la ligne ou il faut tirer
	:param colonne:la colonne ou il faut tirer
	:type tirs: list
	:type ligne: int
	:type colonne: int
	:return: si le tir est possible
	:rtype: bool
	
	>>> tir_valide(tirs,11,18)
	False
	
	"""
	if ligne>10 or colonne>10:
		print("cette case n'est pas dans la grille")
		return False
		
	if tirs[ligne][colonne]!= -1:
		print("tirs deja effectuer sur cette position essayer une autre position")
		return False
	
	return True

def prochain_coup(tirs:list):
	"""
	demande a l'utilisateur le prochain coup et verifie qu'il est valide
	:param tirs: la grille des tirs deja effectuer
	:type tirs: list
	:return: la position ou l'utilisateur veut tirer
	:rtype:tuple
	
	"""
	lignes=['A','B','C','D','E','F','G','H','I','J']
	l=input("donner la ligne a toucher")
	compt=0
	for i in lignes:
		if l==i:
			ligne=compt
		compt+=1
	colonne=int(input("donner la colonne a toucher"))
	colonne-=1
	while tir_valide(tirs,ligne,colonne)== False:
		l=input("donner la ligne a toucher")
		colonne=int(input("donner la colonne a toucher"))
		compt=0
		for i in lignes:
			if l==i:
				ligne=compt
			compt+=1
		colonne-=1
		
	return (ligne,colonne)
	
def resultat_tir(grilleTirs:list,grille:list,ligne:int,colonne:int):
	"""
	verifie et met a jour la grille tirs en fonction de la position du tirs de l'utilisateur
	:param grilleTirs:la grille des tirs avec tout les tirs deja effectuer
	:param grille: la grille des bateaux
	:param ligne: la ligne que l'utilisateur veut toucher
	:param colonne: la colonne que l'utilisateur veut toucher
	:type grilleTirs: list
	:type grille:list
	:type ligne:int
	:type colonne:int
	:return:la nouvelle grille de tirs mis a jours
	:rtype: list
	
	"""
	global comptPA
	global comptCT
	global comptSM
	global comptT
	global comptC
	if grille[ligne][colonne]==3:
		comptPA+=1
		if comptPA==5:
			for i in range(len(grille)):
				for j in range(len(grille[i])):
					if grille[i][j]==3:
						grilleTirs[i][j]=2
		else:
			grilleTirs[ligne][colonne]=1
	elif grille[ligne][colonne]==4:
		comptC+=1
		if comptC==4:
			for i in range(len(grille)):
				for j in range(len(grille[i])):
					if grille[i][j]==4:
						grilleTirs[i][j]=2
		else:
			grilleTirs[ligne][colonne]=1
	elif grille[ligne][colonne]==5:
		comptCT+=1
		if comptCT==3:
			for i in range(len(grille)):
				for j in range(len(grille[i])):
					if grille[i][j]==5:
						grilleTirs[i][j]=2
		else:
			grilleTirs[ligne][colonne]=1
		
	elif grille[ligne][colonne]==6:
		comptSM+=1
		if comptSM==3:
			for i in range(len(grille)):
				for j in range(len(grille[i])):
					if grille[i][j]==6:
						grilleTirs[i][j]=2
		else:
			grilleTirs[ligne][colonne]=1
		
	elif grille[ligne][colonne]==7:
		comptT+=1
		if comptT==2:
			for i in range(len(grille)):
				for j in range(len(grille[i])):
					if grille[i][j]==7:
						grilleTirs[i][j]=2
		else:
			grilleTirs[ligne][colonne]=1
		
	else:
		grilleTirs[ligne][colonne]=0	
	return grilleTirs
	
def partie_finie(tirs:list):
	"""
	veifie si la partie est finie
	
	:param tirs:le tableau des tirs 
	:type tirs:list
	:return:si la partie est finie ou pas
	:rtype:bool
	"""
	compt=0
	for i in tirs:
		for j in i:
			if j==2:
				compt+=1
	if compt==17:
		print("bravo vous avez couler tout les bateaux")
		return True
	return False

def afficher_tirs(tirs:list):
	"""
	affiche le tableau des tirs a l'utilisateur
	:param tirs:le tableau des tirs 
	:type tirs:list
	
	"""
	listecolonne=['',1,2,3,4,5,6,7,8,9,10]
	listeligne=['A','B','C','D','E','F','G','H','I','J']
	afficheTirs=initialiser_grille()
	
	print("\033[5;0H",end='')
	for i in range(len(tirs)):
		for j in range(len(tirs[i])):
			if tirs[i][j]==-1:
				afficheTirs[i][j]="."
			if tirs[i][j]==0:
				afficheTirs[i][j]="*"
			if tirs[i][j]==1:
				afficheTirs[i][j]="+"
			if tirs[i][j]==2:
				afficheTirs[i][j]="X"
	print('', end=' ')
	for i in listecolonne:
		print(i, end=' ')
	print()
	for i in range(len(afficheTirs)):
		print(listeligne[i], end=' ')
		for j in range(len(afficheTirs[i])):
			print(afficheTirs[i][j], end=' ')
		print()

def jouer():
	"""
	permet de jouer au jeu
	"""
	tirs=initialiser_grille()
	bateaux=initialiser_grille()
	bateaux=placer_bateaux(bateaux)
	os.system('clear')
	afficher_tirs(tirs)
	while partie_finie(tirs)==False:
		coup=prochain_coup(tirs)
		tirs=resultat_tir(tirs,bateaux,coup[0],coup[1])
		os.system('clear')
		afficher_tirs(tirs)
	return("bravo tout les bateaux ont coulé")

comptPA=0
comptC=0
comptCT=0
comptSM=0
comptT=0
jouer()
