import copy
MAX_STATE = 0
import json
import sys

demo = {
        "states": [],
        "letters": [],
        "transition_matrix": [],
        "start_states": [],
        "final_states": [],
}

def get_state():
    global MAX_STATE
    MAX_STATE+=1
    return MAX_STATE


def parseInput(regex):
    ans = []
    for i in range(len(regex)):
        if(i==0):
            ans.append(regex[i])
        else:
            if( regex[i-1]!='+' and regex[i-1]!='(' and regex[i] != '+' and regex[i]!='*' and regex[i]!=')'  ):
                ans.append('.')
            ans.append(regex[i])
    return ans


def infixToPostfix(regex):
    alphabet = []
    for char in regex:
        if( (char not in alphabet) and char!='*' and char!='+' and char != '.' and char!='(' and char !=')' ):
            alphabet.append(char)

    stack = []
    output = []

    for i in range(len(regex)):
        # ignore '*'
        if regex[i] == '*':
            output.append(regex[i])

        # char is a letter
        elif regex[i] in alphabet:
            output.append(regex[i])
        
        # opening brace => push to stack
        elif regex[i] == '(':
            stack.append(regex[i])
        
        # closing brace => messy
        elif regex[i] == ')':
            # until you get an a ')'
            while(stack[-1] != '('):
                # add the last element to the output
                output.append(stack.pop())
            #finally you got it so just pop!!
            stack.pop()
        
        # char is '+' or '.'
        else:
            if(regex[i]=='+'):
                while(len(stack) and stack[-1]=='.'):
                    output.append(stack.pop())
            stack.append(regex[i])


    stack.reverse()
    for i in stack:
        output.append(i)
    ans = ''
    for i in output:
        ans+=i

    return ans

def make_nfa(letter):
    ans = copy.deepcopy(demo)
    start = get_state()
    end = get_state()
    transition = [start, letter, end]

    ans["states"].append(start)
    ans["states"].append(end)
    ans["letters"].append(letter)
    ans["transition_matrix"].append(transition)
    ans["start_states"].append(start)
    ans["final_states"].append(end)

    return ans


def do_union(nfa1, nfa2):

    ans = copy.deepcopy(demo)
    new_start = get_state()
    transition1 = [new_start, '$', nfa1["start_states"][0]]
    transition2 = [new_start, '$', nfa2["start_states"][0]]

    ans["states"] = nfa1["states"] + nfa2["states"]
    ans["states"].append(new_start)

    ans["letters"] = list(set(nfa1["letters"] + nfa2["letters"]))

    ans["transition_matrix"] = nfa1["transition_matrix"] + nfa2["transition_matrix"]
    ans["transition_matrix"].append(transition1)
    ans["transition_matrix"].append(transition2)

    ans["start_states"].append(new_start)
    ans["final_states"] = nfa1["final_states"] + nfa2["final_states"]

    return ans

def do_concat(nfa1, nfa2):

    ans = copy.deepcopy(demo)

    ans["states"] = nfa1["states"] + nfa2["states"]

    ans["letters"] = list(set(nfa1["letters"] + nfa2["letters"]))

    ans["transition_matrix"] = (nfa1["transition_matrix"] + nfa2["transition_matrix"])
    for state in nfa1["final_states"]:
        ans["transition_matrix"].append([state, '$', nfa2["start_states"][0]])

    ans["start_states"] = nfa1["start_states"]
    ans["final_states"] = nfa2["final_states"]

    return ans


def do_star(nfa):
    ans = copy.deepcopy(demo)

    new_start = get_state()
    
    ans["states"] = nfa["states"]
    ans["states"].append(new_start)

    ans["letters"] = nfa["letters"]
    ans["transition_matrix"] = nfa["transition_matrix"]
    for state in nfa["final_states"]:
        ans["transition_matrix"].append([state, '$', nfa["start_states"][0]])
    ans["transition_matrix"].append([new_start, '$', nfa["start_states"][0]])
    
    ans["start_states"].append(new_start)

    ans["final_states"] = nfa["final_states"]
    ans["final_states"].append(new_start)

    return ans


def solvePostfix(postfixRegex):
    stack=[]
    for i in range(len(postfixRegex)):
        if(postfixRegex[i]=='+'):
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(do_union(nfa1, nfa2))

        elif(postfixRegex[i]=='.'):
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(do_concat(nfa1, nfa2))
        
        elif(postfixRegex[i]=='*'):
            nfa = stack.pop()
            stack.append(do_star(nfa))

        else:
            stack.append(make_nfa(postfixRegex[i]))

    return stack[-1]




if __name__ == "__main__":

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    f = open(input_file,"r")
    input_regex_dict = json.load(f)
    f.close()



    parsedRegex = parseInput(input_regex_dict["regex"])
    postfixRegex = infixToPostfix(parsedRegex)
    output_nfa = (solvePostfix(postfixRegex))


    f1 = open(output_file,"w")
    json.dump(output_nfa, f1, indent=4)
    f1.close()



