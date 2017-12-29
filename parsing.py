import re
import numpy as np
from collections import defaultdict
from gss.gll import RFA

def get_grammar(filename): # File -> dictionary for productions
    result_dict = defaultdict(list)
    production_pattern = r'(?P<lp>\w) -> (?P<rp>.*)$'
    production = re.compile(production_pattern)  # Regex for productions
    try:
        with open(filename) as f:
            for line in filter(None, f.read().splitlines()):
                match = production.match(line)
                if match:
                    lp = match.group('lp')
                    rp = match.group('rp')
                    rp_splitted = rp.replace(' ', '').split('|')
                    result_dict[lp].extend(rp_splitted)
    except FileNotFoundError:
        print("Can't find file with grammar")
        raise FileNotFoundError
    return {k: ['$'] if v[0] == 'eps' else v for k, v in result_dict.items()}


def get_graph(filename):  # Graph -> np.ndarray (adjacency matrix)
    transition_pattern = r"(?P<lp>\d*) -> (?P<rp>\d*).*\"(?P<label>\d*)\".*"
    transition = re.compile(transition_pattern)
    try:
        with open(filename) as f:
            nodes = [next(f) for _ in range(3)][2]
            shape = nodes.count(';')  # number of nodes
            matrix = np.zeros((shape, shape), dtype=str)
            for line in filter(None, f.read().splitlines()):
                match = transition.match(line)
                if match:
                    fr = int(match.group('lp'))
                    to = int(match.group('rp'))
                    label = match.group('label')
                    matrix[fr, to] = '$' if label == 'eps' else label
    except FileNotFoundError:
        print("Can't find file with graph")
        raise FileNotFoundError
    return matrix


def get_rfa(filename):
    # key_states: nonterm -> dict: {'start' -> set(start_position), 'final' -> set(final_position)}
    # transitions : vertex -> set((vertex, label))
    vertex_descr = r'(?P<vertex>\d*)\[(label="(?P<label>\w*)"|)(, |)(shape="(?P<shape>\w*)"|)(, |)(color="(?P<color>\w*)"|).*\]$'
    trans = r'(?P<from>\d*) -> (?P<to>\d*)\[label="(?P<label>\w*)"\]$'
    transitions = defaultdict(set)
    key_states = defaultdict(lambda: defaultdict(set))
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
                        key_states[label]['final'].add(vertex)

                    if color == "green":
                        key_states[label]['start'].add(vertex)

                if trans_matching:
                    label = trans_matching.group('label')
                    fr = int(trans_matching.group('from'))
                    to = int(trans_matching.group('to'))
                    transitions[fr].add((to, label))
            return RFA({key: dict(value) for key, value in dict(key_states).items()}, dict(transitions))

    except FileNotFoundError:
        print("Can't find file with RFA")
        raise FileNotFoundError
