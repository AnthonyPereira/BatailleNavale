import allumetteEnv

nbAllumette=17
coupPossible=(1,2,3)

def generate():
    morpion1 = allumetteEnv.AllumetteEnv(nbAllumette, 0, coupPossible)
    morpion2 = allumetteEnv.AllumetteEnv(nbAllumette, 1, coupPossible)
    morpion1.generate_p()
    morpion2.generate_p()
    morpion1.save_p("p1.data")
    morpion2.save_p("p2.data")
generate()