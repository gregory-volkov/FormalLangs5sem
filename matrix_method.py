import sys
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

    return [(i, nonterm, j) for i, j in product(range(n), repeat=2) for nonterm in gram_matrix[i, j]]

if len(sys.argv) > 1:
    res = grammar_closure(get_grammar(sys.argv[1]), get_graph(sys.argv[2]))
    res_str = '\n'.join([','.join([str(i), nonterm, str(j)]) for i, nonterm, j in res])
    if len(sys.argv) > 3:
        with open(sys.argv[3]) as f:
            f.write(res_str)
            f.close()
    else:
        sys.stdout.write(res_str + '\n')
