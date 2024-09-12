import numpy as np

def is_final_state(state, final_states):
    if state not in final_states:
        return False
    else:
        return True

def get_transition(state, letter, transitions):
    for transition in transitions:
        if transition[0] == state and transition[1] == letter:
            return transition[2]

    return 100

def get_final_states(non_colourable, states):
    final_states = []
    for array in non_colourable:
        for mar_key, mar_value in states.items():
            if np.array_equal(mar_value, array):
                final_states.append(mar_key)
                continue

    return final_states