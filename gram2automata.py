from gss.gll import RFA
from parsing import get_grammar
from collections import defaultdict


def gram2automata(gram):
    key_states = defaultdict(lambda: defaultdict(set))
    transitions = defaultdict(set)
    max_state = 0
    for nonterm in gram:
        start_state = max_state
        max_state += 1
        key_states[nonterm]['start'].add(start_state)
        for right_part in gram[nonterm]:
            cur_state = start_state
            for symbol in right_part:
                    transitions[cur_state].add((max_state + 1, symbol))
                    max_state += 1
                    cur_state = max_state
            key_states[nonterm]['final'].add(cur_state)
        max_state += 1
    return RFA(key_states, transitions)