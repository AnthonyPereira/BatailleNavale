import DeepConvo
import morpionMCenv


print("AI Training")

nb_swap = int(input("How many AI swap for training ? : "))      # selection du nombre de swap
nb_episode = int(input("How many game per training ? : "))      # selection du nombre d'episode d'un swap

morpion1 = morpionMCenv.MorpionMCEnv(0)                         # initialisation environnement joueur 1
morpion2 = morpionMCenv.MorpionMCEnv(1)                         # initialisation environnement joueur 2

print("Training started ..")

DeepConvo.train_ia(morpion1, morpion2, nb_swap, nb_episode)     # commencer l'entrainement

print("2 file was create with name : ' ./save/convo/episode.ckpt ' and the number of the AI player")