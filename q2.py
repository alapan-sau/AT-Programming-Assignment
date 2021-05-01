import json
import sys

input_nfa = {}

if __name__ == '__main__':

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    f = open(input_file,"r")
    input_nfa = json.load(f)
    f.close()



    output_dfa = {
        "states": [
        ],
        "letters": [
        ],
        "transition_function": [],
        "start_states": [],
        "final_states": [],
    }

    power_states = []

    num_states = len(input_nfa["states"])

    for i in range(2**num_states):
        power_states.append([])
        for j in range(num_states):
            if( ((i & (1 << (j))) >> (j)) ):
                power_states[i].append(input_nfa["states"][j])


    output_dfa["letters"] = list(input_nfa["letters"])

    output_dfa["states"] = []
    for i in range(2**num_states):
        output_dfa["states"].append(list(power_states[i]))


    output_dfa["start_states"] = []
    output_dfa["start_states"].append([ input_nfa["start_states"][0] ])

    output_dfa["transition_function"] = []
    for state in output_dfa["states"]:
        for letter in output_dfa["letters"]:
            destination = []

            # every NFA state
            for individual in state:
                # find the transition and append the result DFA state
                for nfa_transition in input_nfa["transition_function"]:
                    if(nfa_transition[0] == individual and nfa_transition[1] == letter):
                        destination.append(nfa_transition[2])

            output_dfa["transition_function"].append([state, letter, destination])


    output_dfa["final_states"] = []
    for state in output_dfa["states"]:
        flag = 0
        for individual in state:
            if(individual in input_nfa["final_states"]):
                flag=1
                break

        if(flag):
                output_dfa["final_states"].append(state)

    # print(output_dfa)

    f1 = open(output_file,"w")
    json.dump(output_dfa, f1, indent=4)
    f1.close()