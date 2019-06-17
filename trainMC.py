import pickle

import iaMC2
import os
import generate_3_by_3_env
from pathlib import Path
import morpionMCenv

print("AI Training")

nb_swap = int(input("How many AI swap for training ? : "))
nb_episode = int(input("How many game per training ? : "))
gamma = 1.0
alpha = 0.9
name = ""

if input("Do you wish to name the IA ? y / n : ") == "y":
    name = input("name ? : ")

print("Checking if everything is OK before training ..")
ia_folder = Path('./ia')
data = Path('./p1.data')

if not data.is_file():
    print("p.data missing")
    print("Generating 3 by 3 env ..", end='')
    generate_3_by_3_env.generate()
    print("Done !")
if not ia_folder.is_dir():
    print("ia folder missing")
    print("Generating ia folder")
    os.mkdir("ia")

morpion1 = morpionMCenv.MorpionMCEnv(0)
morpion2 = morpionMCenv.MorpionMCEnv(1)


print("Training started ..")
ia_name = name + "_"  + "_" + str(nb_swap) + "_" + str(nb_episode) + "_" + str(gamma)
iaMC2.train_ia(morpion1, morpion2, nb_swap, nb_episode, alpha)

print("Training done ..")
print("Saving..")

file1 = open("./ia/ckpt/" + "0", "rb")
file2 = open("./ia/ckpt/" + "1", "rb")

morpion1.save_env("./ia/ia1_"+ia_name, pickle.load(file1))
morpion2.save_env("./ia/ia2_"+ia_name, pickle.load(file2))
file1.close()
file2.close()
print("IA saved as")
