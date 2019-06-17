import ia
import os
import random
import generate_3_by_3_env
from pathlib import Path
import morpionEnv

print("AI Training")

max_it = int(input("How many iteration for policy evaluation ? : "))
nb_swap = int(input("How many AI swap for training ? : "))
nb_train = int(input("How many iteration per training ? : "))
gamma = 1.0
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

morpion1 = morpionEnv.MorpionEnv(3, 0)
morpion2 = morpionEnv.MorpionEnv(3, 1)
morpion1.load_p("p1.data")
morpion2.load_p("p2.data")

morpion1.generate_random_policy()
morpion2.generate_random_policy()

morpion1.generate_v()
morpion2.generate_v()

random.seed()

print("Training started ..")

ia.train_ia(morpion1, morpion2, nb_swap, max_it, nb_train, gamma)

print("Training done ..")
print("Saving..")
ia_name = name + "_" + str(max_it) + "_" + str(nb_swap) + "_" + str(nb_train) + "_" + str(gamma)
morpion1.save_env("./ia/ia1_" + ia_name)
morpion2.save_env("./ia/ia2_" + ia_name)
print("IA saved as " + ia_name)
