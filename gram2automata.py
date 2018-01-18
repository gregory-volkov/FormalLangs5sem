from gss.gll import RFA
from parsing import get_grammar
from collections import defaultdict


def gram2automata(gram):
    key_states = defaultdict(lambda: defaultdict(set))
    transitions = defaultdict(set)
    start_states = defaultdict(set)
    final_states = defaultdict(set)
    max_state = 0
    for nonterm in gram:
        start_state = max_state
        max_state += 1
        start_states[nonterm].add(start_state)
        for right_part in gram[nonterm]:
            cur_state = start_state
            for symbol in right_part:
                    transitions[cur_state].add((max_state + 1, symbol))
                    max_state += 1
                    cur_state = max_state
            final_states[nonterm].add(cur_state)
        max_state += 1
    return RFA(start_states, final_states, transitions)