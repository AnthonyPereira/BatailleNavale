import DeepMCvsBaleze

state = ()

while True:
    action = DeepMCvsBaleze.nextAction(0, state)
    state = state + (action,)
    print(state)
    state = state + (int(input()),)
