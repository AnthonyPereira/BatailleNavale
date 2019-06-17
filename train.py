import ia
import os
import random
import generate
from pathlib import Path
import allumetteEnv
from trainJeu import nbAllumette,coupPossible


print("AI Training")

max_it = 5
nb_swap = 5
nb_train = 5
gamma = 1.0
name = ""



print("Checking if everything is OK before training ..")
ia_folder = Path('./ia')
data = Path('./p1.data')

if not data.is_file():
    print("p.data missing")
    print("Generating 3 by 3 env ..", end='')
    generate.generate()
    print("Done !")
if not ia_folder.is_dir():
    print("ia folder missing")
    print("Generating ia folder")
    os.mkdir("ia")


morpion1 = allumetteEnv.AllumetteEnv(nbAllumette, 0,coupPossible)
morpion2 = allumetteEnv.AllumetteEnv(nbAllumette, 1,coupPossible)
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

cp = ""
for i in coupPossible:
    cp = cp + str(i) + "_"

ia_name = str(name) + "_" + str(cp) +"_" + str(nbAllumette) + "_" + str(max_it) + "_" + str(nb_swap) + "_" + str(nb_train) + "_" + str(gamma)
morpion1.save_env("./ia/ia1_" + ia_name)
morpion2.save_env("./ia/ia2_" + ia_name)
print("IA saved as " + ia_name)
