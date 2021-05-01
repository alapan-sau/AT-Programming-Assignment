import json
import sys

unreachable_dfa = {}


def get_transition(q, c):
    for i in unreachable_dfa["transition_function"]:
        if(i[0] == q and i[1] == c):
            return i[2]


def make_reachable():
    reachable_states = [unreachable_dfa["start_states"][0]]
    new_states = [unreachable_dfa["start_states"][0]]

    while(len(new_states)):
        temp = []
        for state in new_states:
            for c in unreachable_dfa["letters"]:
                p = get_transition(state, c)
                if(p not in temp):
                    temp.append(p)
        
        new_states = []
        for i in temp:
            if(i not in reachable_states):
                new_states.append(i)
        
        for i in new_states:
            if(i not in reachable_states):
                reachable_states.append(i)
    
    unreachable_states = []
    for i in unreachable_dfa["states"]:
        if(i not in reachable_states):
            unreachable_states.append(i)

    reachable_dfa = {}

    reachable_dfa["letters"] = list(unreachable_dfa["letters"])
    reachable_dfa["states"] = list(reachable_states)

    reachable_dfa["start_states"] = list(unreachable_dfa["start_states"] )
    reachable_dfa["final_states"] = []

    for i in unreachable_dfa["final_states"]:
        if(i in reachable_states):
            reachable_dfa["final_states"].append(i)
    

    reachable_dfa["transition_function"] = []
    for i in unreachable_dfa["transition_function"]:
        if( (i[0] in reachable_states) and (i[2] in reachable_states) ):
            reachable_dfa["transition_function"].append(i)

    return reachable_dfa


def hopcroft(dfa):
    final = list(dfa["final_states"])
    non_final = []
    for i in dfa["states"]:
        if(i not in final):
            non_final.append(i)

    P = []
    W = []
    P.append(final)
    P.append(non_final)
    W.append(final)
    W.append(non_final)

    while(len(W)):
        A = W.pop()
        for c in dfa["letters"]:
            X = []
            for transition in dfa["transition_function"]:
                if(transition[1] == c and (transition[2] in A)):
                    X.append(transition[0])
            
            removals = []
            intersections = []
            differences = []

            for Y in P:
                intersection = []
                difference = []

                for i in Y:
                    if(i in X):
                        intersection.append(i)
                    else:
                        difference.append(i)

                if(len(intersection) and len(difference)):
                    removals.append(Y)
                    differences.append(difference)
                    intersections.append(intersection)

            for i in range(len(removals)):
                P.remove(removals[i])
                P.append(intersections[i])
                P.append(differences[i])

            
                if(removals[i] in W):
                    W.remove(removals[i])
                    W.append(intersections[i])
                    W.append(differences[i])    
                else:
                    if len(intersections[i]) <= len(differences[i]):
                        W.append(intersections[i])
                    else:
                        W.append(differences[i])    


    result_dfa = {}
    result_dfa["letters"] = list(dfa["letters"])
    result_dfa["states"] = list(P)
    result_dfa["start_states"] = []
    for i in P:
        if(dfa["start_states"][0] in i):
            result_dfa["start_states"].append(i)
            break

    result_dfa["final_states"] = []
    for state in dfa["final_states"]:
        for i in P:
            if(state in i and i not in result_dfa["final_states"]):
                result_dfa["final_states"].append(i)      


    result_dfa["transition_function"] = []
    for transition in dfa["transition_function"]:
        for i in P:
            if(transition[0] in i):
                state1 = i
            if(transition[2] in i):
                state2 = i

        if( [state1, transition[1], state2] not in result_dfa["transition_function"] ):
            result_dfa["transition_function"].append([state1, transition[1], state2])
        
        
    # result_dfa["transition_function"] = list(set( result_dfa["transition_function"] ))
    return result_dfa

        
if __name__ == '__main__':

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    f = open(input_file,"r")
    unreachable_dfa = json.load(f)
    f.close()


    ans = (hopcroft(make_reachable()))

    f1 = open(output_file,"w")
    json.dump(ans, f1, indent=4)
    f1.close()