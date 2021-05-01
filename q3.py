import copy
import json
import sys

input_dfa = {}


### regex_operations
PHI = "()"

def union_regex(reg1 , reg2):
    if reg1 == PHI:
        return reg2
    if reg2 == PHI:
        return reg1
    return "(" + reg1 +  "+" +  reg2 + ")"

def concat_regex(reg1, reg2):
    if reg1 == PHI or reg2 == PHI:
        return PHI

    return "(" + reg1 + reg2 + ")"

def star_regex(reg):
    if(reg == PHI):
        return PHI
    return "(" + reg + "*"+ ")"



def generate_regex( initial_gnfa ):

    k = len(initial_gnfa["states"])
    gnfa = initial_gnfa

    while(k > 2):
        lower_gnfa = {}

        for selected_state in gnfa["states"]:
            if(selected_state != 'S' and selected_state != 'E'):
                break
        
        # added states
        lower_gnfa["states"] = []
        for state in gnfa["states"]:
            if(state != selected_state):
                lower_gnfa["states"].append(state)
        
        lower_gnfa["letters"] = list(gnfa["letters"])
        lower_gnfa["start_states"] = [["S"]] #start state
        lower_gnfa["final_states"] = [["E"]] #end state


        # add the transitions related to selected_state
        incoming = [] # regex, state
        outgoing = []
        self_regex = PHI
        for transition in gnfa["transition_function"]:
            if(transition[0] == selected_state and transition[2] == selected_state):
                self_regex = transition[1]
            elif(transition[0] == selected_state):
                outgoing.append([transition[1], transition[2]])
            elif(transition[2] == selected_state):
                incoming.append([transition[1], transition[0]])
        

        lower_gnfa["transition_function"] = []
        for state1 in gnfa["states"]:
            if(state1 == selected_state or state1 == 'E'):
                continue
            for state2 in gnfa["states"]:
                if(state2 == selected_state or state2 == 'S'):
                    continue
                char  = PHI
                ## search for the corresponding direct transition
                for transition in gnfa["transition_function"]:
                    if(transition[0] == state1 and transition[2] == state2):
                        char = transition[1]
                        break
                
                R1 = PHI
                R2 = PHI
                for i in incoming:
                    if(i[1] == state1):
                        R1 = i[0]

                for i in outgoing:
                    if(i[1] == state2):
                        R2 = i[0]

                
                temp = concat_regex(R1, star_regex(self_regex))

                new_path = concat_regex( concat_regex(R1, star_regex(self_regex) ) , R2)
                char = union_regex(char, new_path)

                lower_gnfa["transition_function"].append([state1, char, state2])

        gnfa = copy.deepcopy(lower_gnfa)
        k = len(gnfa["states"])
    
    return gnfa["transition_function"][0][1]


if __name__ == '__main__':

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    f = open(input_file,"r")
    input_dfa = json.load(f)
    f.close()



    initial_gnfa = {
    "states": [],
    "letters": [],
    "transition_function": [],
    "start_states": [],
    "final_states": []
    }

    initial_gnfa["states"] = list(input_dfa["states"])
    initial_gnfa["states"].append("S")
    initial_gnfa["states"].append("E")

    initial_gnfa["letters"] = list(input_dfa["letters"])
    initial_gnfa["start_states"] = [["S"]] #start state
    initial_gnfa["final_states"] = [["E"]] #end state

    # generate the transition like a bond

    transition = []
    ## add the start and end arrows
    transition.append(['S', '($)', input_dfa["start_states"][0] ])

    for i in input_dfa["final_states"]:
        transition.append([i, '($)', 'E'])

    ## add all state_state transitions and make them regex:

    for state1 in input_dfa["states"]:
        for state2 in input_dfa["states"]:
            char  = PHI
            for dfa_trans in input_dfa["transition_function"]:
                if(dfa_trans[0] == state1 and dfa_trans[2] == state2):
                    reg_init = "(" + dfa_trans[1] + ")"
                    char = union_regex(char,  reg_init)
            if(state1 == state2 and char == PHI):
                    char = '($)'
        
            transition.append([state1, char, state2])

        ## attach to start state
        if(state1 != input_dfa["start_states"][0]):
            transition.append(['S', PHI, state1])
        
        ## attach to end state
        if(state1 not in input_dfa["final_states"]):
            transition.append([state1, PHI, 'E'])
        
        ## start-end
            transition.append(['S', PHI, 'E'])
        

    initial_gnfa["transition_function"] = list(transition)

    ans = (generate_regex(initial_gnfa))

    ans_dict = {}
    ans_dict["regex"] = ans

    f1 = open(output_file,"w")
    json.dump(ans_dict, f1, indent=4)
    f1.close()