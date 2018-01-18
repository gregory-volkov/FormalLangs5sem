import re
import numpy as np
from collections import defaultdict
from gss.gll import RFA


def get_grammar(filename): # File -> dictionary for productions
    result_dict = defaultdict(lambda: list(list()))
    production_pattern = r'(?P<lp>(\w|\d)*) -> (?P<rp>.*)$'
    production = re.compile(production_pattern)  # Regex for productions
    try:
        with open(filename) as f:
            for line in filter(None, f.read().splitlines()):
                match = production.match(line)
                if match:
                    lp = match.group('lp')
                    rp = match.group('rp')
                    rp_splitted = rp.split()
                    result_dict[lp].append(rp_splitted)
    except FileNotFoundError:
        print("Can't find file with grammar")
        raise FileNotFoundError
    return dict(result_dict)


def get_graph(filename):  # Graph -> np.ndarray (adjacency matrix)
    transition_pattern = r"(?P<lp>\d*) -> (?P<rp>\d*).*\"(?P<label>\w*)\".*"
    transition = re.compile(transition_pattern)
    try:
        with open(filename) as f:
            adj_list = defaultdict(lambda: defaultdict(set))
            for line in filter(None, f.read().splitlines()):
                match = transition.match(line)
                if match:
                    fr = int(match.group('lp'))
                    to = int(match.group('rp'))
                    label = match.group('label')
                    adj_list[fr][to].add(label)
    except FileNotFoundError:
        print("Can't find file with graph")
        raise FileNotFoundError
    return adj_list


def get_rfa(filename):
    # key_states: nonterm -> dict: {'start' -> set(start_position), 'final' -> set(final_position)}
    # transitions : vertex -> set((vertex, label))
    vertex_descr = r'(?P<vertex>\d*)\[(label="(?P<label>\w*)"|)(, |)(shape="(?P<shape>\w*)"|)(, |)(color="(?P<color>\w*)"|).*\]$'
    trans = r'(?P<from>\d*) -> (?P<to>\d*)\[label="(?P<label>\w*)"\]$'
    transitions = defaultdict(set)
    start_states = defaultdict(set)
    final_states = defaultdict(set)
    vertex_descr_regex = re.compile(vertex_descr)
    trans_regex = re.compile(trans)
    try:
        with open(filename) as f:
            for line in filter(None, f.read().splitlines()):

                descr_matching = vertex_descr_regex.match(line)
                trans_matching = trans_regex.match(line)

                if descr_matching:
                    label = descr_matching.group('label')
                    shape = descr_matching.group('shape')
                    color = descr_matching.group('color')
                    vertex = int(descr_matching.group('vertex'))

                    if shape == "doublecircle":
                        final_states[label].add(vertex)

                    if color == "green":
                        start_states[label].add(vertex)

                if trans_matching:
                    label = trans_matching.group('label')
                    fr = int(trans_matching.group('from'))
                    to = int(trans_matching.group('to'))
                    transitions[fr].add((to, label))
            return RFA(start_states, final_states, dict(transitions))

    except FileNotFoundError:
        print("Can't find file with RFA")
        raise FileNotFoundError
