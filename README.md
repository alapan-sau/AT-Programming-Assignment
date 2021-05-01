# Programming Assignment | Automata Theory

## Q1. Conversion from Regex to NFA

Firstly, the given infix regex expression is parsed by adding the concatenation operators in the `parseInput()` and then it is converted to a postfix regex expression to remove braces in the `infixToPostfix()`<br>

Each individual character in the postfix regex expression is converted into a simple nfa by `make_nfa()`. <br>

The regex is evaluated by solving the postfix expression in `solvePostfix()`. Utility functions like `do_union(), do_concat(), do_star()` are used evaluate union, concatenation and star operations on NFAs to generate new NFAs.<br>

The solution of the postfix expression is the required NFA.

## Q2. Conversion from NFA to DFA:

Initially a Power Set of the states in the NFA is constructed as follows:

```python
    power_states = []

    num_states = len(input_nfa["states"])

    for i in range(2**num_states):
        power_states.append([])
        for j in range(num_states):
            if( ((i & (1 << (j))) >> (j)) ):
                power_states[i].append(input_nfa["states"][j])

```

Each element of the Power Set is a state in the DFA.<br>
The start state of the DFA is the set containing the start state of NFA alone.<br>
The final states of DFA are the sets, which contains atleast one accept state of the NFA.<br>
The transition table is reconstructed from the one from NFA as follows:

```python
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
```

## Q3. Conversion from DFA to Regex

The given DFA is first used to generate a GNFA, `initial_gnfa`. The initially constructed GNFA is reduced to a 2-state GNFA in the `generate_regex()` function. The final regex on the transition from state 'S' to 'E' is then returned as requierd regex.<br><br>

Note: We assume no state is represented as 'S' and 'E' is given in the DFA.<br>

## Q4. Minimising DFA

Firstly we eliminate the non-reachable states in the given DFA and also eliminate the corresponding transition functions involving the eliminated states in the `make_reachable()`.<br>
The reachable DFA is then iterated through the Hofcroft's Algorithm so that the states are partitioned in to sets containing non-distinguishable states in `hopcroft()`.