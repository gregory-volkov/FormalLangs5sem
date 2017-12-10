from parsing import *
import numpy as np
from string import digits, ascii_lowercase
from itertools import product


def grammar_closure(gram, matrix):
    n = matrix.shape[0]
    term_grammar = {}
    for v in gram.values():
        if v[0] in digits + ascii_lowercase:
            num = v[0]
            if num not in term_grammar:
                term_grammar[num] = [k for k, v in gram.items() if num in v]

    # dict: nonterm (concat) nonterm -> nonterm
    nonterm_grammar = {y.replace(' ', ''): x for x, lst in gram.items() for y in lst if y not in digits + ascii_lowercase}

    # function: term -> [nonterm]
    term2nonterm = lambda x: term_grammar.get(x, []).copy()

    # init matrix with [nonterminal] elments
    gram_matrix = np.empty((n, n), dtype=object)
    for i, j in product(range(n), repeat=2):
        gram_matrix[i, j] = term2nonterm(matrix[i, j])

    """
    First variant of gram_matrix define. Problems with matrix of empty lists
    gram_matrix = np.array([term2nonterm(item) for row in matrix for item in row], dtype=object)\
        .reshape((n, n))
    """

    # transitive closure while smth changes in gram_matrix
    stop = False

    while not stop:
        stop = True
        for snd, fst, thd in product(range(n), repeat=3):
            edge_1 = gram_matrix[fst, snd]
            edge_2 = gram_matrix[snd, thd]
            for nonterm_pair in map(lambda x: x[0] + x[1], product(edge_1, edge_2)): # list comprehension +
                if nonterm_pair in nonterm_grammar:
                    nonterm_res = nonterm_grammar[nonterm_pair]
                    if nonterm_res not in gram_matrix[fst, thd]:
                        gram_matrix[fst, thd] += nonterm_res
                        stop = False

    # number of 'S' in matrix
    return [(i, 'S', j) for i, j in product(range(n), repeat=2) if 'S' in gram_matrix[i,j]]