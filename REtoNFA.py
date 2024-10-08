class Transitions:
    def __init__(self, start, symbol, end):
        self.start = start
        self.symbol = symbol
        self.end = end

    def __str__(self):
        return f"({self.start}, {self.symbol}) -> {self.end}"

class NFA:
    def __init__(self, startState, acceptState):
        self.startState = startState
        self.acceptState = acceptState
        self.transitions = []

    def addTransition(self, start, symbol, end):
        self.transitions.append(Transitions(start,symbol,end))
    
    def __str__(self):
        #sorts transitions based on their start state
        sortedTransitions = sorted(self.transitions, key=lambda t: (t.start, t.symbol, t.end))
        transitionStr = "\n".join(str(t) for t in sortedTransitions)
        return f"Start: {self.startState}\nAccept: {self.acceptState}\n{transitionStr}"

def createNFA(symbol, stateCounter):
    startState = f'q{stateCounter}'
    acceptState = f'q{stateCounter + 1}'
    nfa = NFA(startState, acceptState)
    nfa.addTransition(startState, symbol, acceptState)
    print(f"Created NFA for symbol '{symbol}': start={startState}, accept={acceptState}")
    return nfa, stateCounter + 2

#concatenates 2 NFAs by adding a epsilon transition from the accept state of NFA1 to the start state of NFA2
def concatenateNFA(nfa1, nfa2):
    print(f"Concatenating NFA1: start={nfa1.startState}, accept={nfa1.acceptState} with NFA2: start={nfa2.startState}, accept={nfa2.acceptState}")

    nfa1.addTransition(nfa1.acceptState, 'E', nfa2.startState)
    #updates accept state
    nfa1.acceptState = nfa2.acceptState
    nfa1.transitions += nfa2.transitions
    print(f"After concatenation: new accept={nfa1.acceptState}")

    return nfa1

def unionNFA(nfa1, nfa2, stateCounter):
    #creates new start and accept state
    startState = f'q{stateCounter}'
    acceptState = f'q{stateCounter + 1}'
    updatedNFA = NFA(startState, acceptState)

    #adds epsilon transitions from new start state to nfa1 and nfa2 start states
    updatedNFA.addTransition(startState, 'E', nfa1.startState)
    updatedNFA.addTransition(startState, 'E', nfa2.startState)

    #same with accept states
    updatedNFA.addTransition(nfa1.acceptState, 'E', acceptState)
    updatedNFA.addTransition(nfa2.acceptState, 'E', acceptState)

    #combines transitions from nfa1 and nfa2s
    updatedNFA.transitions += nfa1.transitions + nfa2.transitions
    print(f"Union NFA created: start={startState}, accept={acceptState}")

    return updatedNFA, stateCounter + 2

def kleeneStarNFA(nfa, stateCounter):
    #creates new start and accept state
    startState = f'q{stateCounter}'
    acceptState = f'q{stateCounter + 1}'
    updatedNFA = NFA(startState, acceptState)

    #adds epsilon transitions
    updatedNFA.addTransition(startState, 'E', nfa.startState)
    updatedNFA.addTransition(startState, 'E', acceptState)
    updatedNFA.addTransition(nfa.acceptState, 'E', nfa.startState)
    updatedNFA.addTransition(nfa.acceptState, 'E', acceptState)
    #combines transitions
    updatedNFA.transitions += nfa.transitions
    print(f"Kleene star NFA created: start={startState}, accept={acceptState}")

    return updatedNFA, stateCounter + 2

def processPostfixExpression(expr):
    stack = []
    stateCounter = 1  #start state numbering from q1
    validSymbols = {'a', 'b', 'c', 'd', 'e', '|', '&', '*', 'E'}


    for char in expr:
        if char not in validSymbols:
            print(f"Error: Invalid symbol '{char}' in input")
            sys.exit(1)

        if char in {'a', 'b', 'c', 'd', 'e', 'E'}:
            #create an NFA for a single symbol and update the state counter
            nfa, stateCounter = createNFA(char, stateCounter)
            stack.append(nfa)
        elif char == '&':
            if len(stack) < 2:
                print("Error: Malformed input")
                sys.exit(1)
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concatenateNFA(nfa1, nfa2))
        elif char == '|':
            # union creates two new states, so stateCounter is incremented
            if len(stack) < 2:
                print("Error: Malformed input")
                sys.exit(1)
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            new_nfa, stateCounter = unionNFA(nfa1, nfa2, stateCounter)
            stack.append(new_nfa)
        elif char == '*':
            # kleene star creates two new states, so stateCounter is incremented
            if len(stack) < 1:
                print("Error: Malformed input")
                sys.exit(1)
            nfa = stack.pop()
            new_nfa, stateCounter = kleeneStarNFA(nfa, stateCounter)
            stack.append(new_nfa)

    if len(stack) != 1:
        print("Error: Malformed input")
        sys.exit(1)

    #returns the new NFA
    final_nfa = stack.pop()
    print(f"Final NFA created with start={final_nfa.startState} and accept={final_nfa.acceptState}")
    return final_nfa

def main(input_file):
    try:
        with open(input_file, 'r') as file:
            for line in file:
                expr = line.strip()
                if expr:
                    print(f"RE: {expr}")
                    nfa = processPostfixExpression(expr)
                    print(nfa)
                    print()
                else:
                    print("skip empty expression")
    except FileNotFoundError:
        print(f"Error: file '{input_file}' not found")
    except Exception as e:
        print(f"Error occured: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Error: no input file")
        sys.exit(1)

    else:
        input_file = sys.argv[1]
        main(input_file)