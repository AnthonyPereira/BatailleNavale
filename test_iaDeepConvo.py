from DeepConvo import nextAction

state = ()

while True:
    action = nextAction(0, state)
    state = state + (action,)
    print(state)
    state = state + (int(input()),)


