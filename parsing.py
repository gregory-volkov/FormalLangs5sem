import re
import numpy as np
from collections import defaultdict


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
                    rp_splitted = rp.split(' | ')
                    result_dict[lp].extend(rp_splitted)
    except FileNotFoundError:
        print("Can't find the file")
        return None
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
        print("Can't find the file")
        return None
    return matrix
