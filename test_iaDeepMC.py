import DeepMC

state = ()

while True:

    state = state + (int(input()),)
    action = DeepMC.nextAction(1, state)
    state = state + (action,)
    print(state)



