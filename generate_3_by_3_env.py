import morpionEnv


def generate():
    morpion1 = morpionEnv.MorpionEnv(3, 0)
    morpion2 = morpionEnv.MorpionEnv(3, 1)
    morpion1.generate_p()
    morpion2.generate_p()
    morpion1.save_p("p1.data")
    morpion2.save_p("p2.data")
generate()