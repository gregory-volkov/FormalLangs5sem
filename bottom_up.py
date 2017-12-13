import numpy as np
from parsing import get_graph, get_grammar
import re
from itertools import product
from string import ascii_uppercase
import sys


def new_path_add(matrix, start, final, s, rules):
    for lp, rp in rules.items():
        if s == lp:
            matrix[start, final].add(rp)


def new_dfs(matrix, start_pos, cur_pos, s, rules, depth=1):
    new_path_add(matrix, start_pos, cur_pos, s, rules)
    if depth == 0:
        return

    n = matrix.shape[0]
    for i in filter(lambda x: bool(matrix[cur_pos, x]), range(n)):
        letters = matrix[cur_pos, i].copy()
        for item in letters:
            new_dfs(matrix, start_pos, i, s + item, rules, depth - 1)


def bottom_up(gram, matrix):
    n = matrix.shape[0]

    res_mat = np.array([set(term) if term else set()
                        for row in matrix
                        for term in row
                        ]).reshape((n, n))

    term_str_regex = re.compile(
        r"([0-9]|[a-z])+$"
    )

    nonterm_str_regex = re.compile(
        r"[A-Z]+"
    )

    term_dict = {term_str: nonterm
                 for nonterm, rp_prod in gram.items()
                 for term_str in rp_prod
                 if term_str_regex.match(term_str)
                 }

    nonterm_dict = {nonterm_str: nonterm
                    for nonterm, rp_prod in gram.items()
                    for nonterm_str in rp_prod
                    if nonterm_str_regex.search(nonterm_str)
                    }

    max_term_len = max(len(term_str) for term_str in term_dict)
    max_nonterm_len = max(len(nonterm_str) for nonterm_str in nonterm_dict)
    # treminal strings substitution
    for i in range(n):
        new_dfs(res_mat, i, i, '', term_dict, max_term_len)

    res_set = set((i, symbol, j) for i, j in product(range(n), repeat=2) for symbol in res_mat[i, j])
    smth_changes = True

    while smth_changes:
        for i in range(n):
            new_dfs(res_mat, i, i, '', nonterm_dict, max_nonterm_len)
        new_set = set((i, symbol, j) for i, j in product(range(n), repeat=2) for symbol in res_mat[i, j])
        if res_set == new_set:
            smth_changes = False
        else:
            res_set = new_set.copy()

    return list(filter(lambda x: x[1] in ascii_uppercase, res_set))


if len(sys.argv) > 1:
    res = bottom_up(get_grammar(sys.argv[1]), get_graph(sys.argv[2]))
    res_str = '\n'.join([','.join([str(i), nonterm, str(j)]) for i, nonterm, j in res])
    if len(sys.argv) > 3:
        with open(sys.argv[3]) as f:
            f.write(res_str)
            f.close()
    else:
        sys.stdout.write(str(res_str.count('S')) + '\n')