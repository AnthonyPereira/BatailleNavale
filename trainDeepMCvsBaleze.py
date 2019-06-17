import pickle
import DeepMCvsBaleze
import morpionMCenv


file = open("./ia/ia2__5_5_5_1.0", "rb")
print("AI Training")

nb_episode = int(input("How many game per training ? : "))      # selection du nombre d'episode d'un swap

morpion1 = morpionMCenv.MorpionMCEnv(0)                         # initialisation environnement joueur 1
morpion2 = pickle.load(file)                                    # recuperation de la politique de joueur 2


print("Training started ..")

DeepMCvsBaleze.train_ia(morpion1, morpion2, nb_episode)    # commencer l'entrainement

print("1 file was create with name : ' ./save/episode.ckpt ' and the number of the AI player")