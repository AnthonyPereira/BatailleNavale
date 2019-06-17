import pickle
import MCvsBaleze
import morpionMCenv
from pathlib import Path

print("AI Training")

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
file = open("./ia/ia2__5_5_5_1.0", "rb")
morpion2 = pickle.load(file)
file.close()

print("Training started ..")
MCvsBaleze.train_ia(morpion1, morpion2, nb_episode, alpha)

print("Training done ..")
print("Saving..")

file1 = open("./ia/ckpt/"+"0", "rb")

morpion1.save_env("./ia/ia1_", pickle.load(file1))
file1.close()
print("IA saved")
