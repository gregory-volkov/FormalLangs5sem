import sys
from parsing import *
import numpy as np
from string import digits, ascii_lowercase
from itertools import product

def grammar_closure(gram, adj_list):

    nonterms = set(gram.keys())
    num2nonterm = dict(enumerate(nonterms))
    nonterm2num = {v: k for k, v in num2nonterm.items()}

    # dict: (non_num, non_num) -> non_num
    nonterm_grammar = defaultdict(set)
    for nonterm, rp_set in gram.items():
        for rp_rule in rp_set:
            if len(rp_rule) == 2:
                nonterm_grammar[(nonterm2num[rp_rule[0]], nonterm2num[rp_rule[1]])].add(nonterm2num[nonterm])

    # dict: term -> non_num
    term2nonterm = defaultdict(set)
    for nonterm, rp_set in gram.items():
        for rp_rule in rp_set:
            if len(rp_rule) == 1:
                term2nonterm[rp_rule[0]].add(nonterm2num[nonterm])

    res_adj_list = defaultdict(lambda: defaultdict(set))
    # init matrix with set(non_num) elments
    for fr in adj_list:
        for to in adj_list[fr]:
            for term in adj_list[fr][to]:
                nonterm_set = term2nonterm[term]
                res_adj_list[fr][to].update(nonterm_set)
    # transitive closure while smth changes in gram_matrix
    stop = False

    while not stop:
        stop = True
        for fst in list(res_adj_list):
            for snd in list(res_adj_list[fst]):
                for thd in list(res_adj_list[snd]):
                    for nonterm_pair in product(res_adj_list[fst][snd], res_adj_list[snd][thd]):
                        if nonterm_pair in nonterm_grammar:
                            res_nonterm_set = nonterm_grammar[nonterm_pair]
                            target_set = res_adj_list[fst][thd]
                            if not res_nonterm_set.issubset(target_set):
                                target_set.update(res_nonterm_set)
                                stop = False

    return [(i, num2nonterm[number], j) for i in res_adj_list for j in res_adj_list[i] for number in res_adj_list[i][j]]

if len(sys.argv) > 1:
    res = grammar_closure(get_grammar(sys.argv[1]), get_graph(sys.argv[2]))
    res_str = '\n'.join([','.join([str(i), nonterm, str(j)]) for i, nonterm, j in res])
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w') as f:
            f.write(res_str)
            f.close()
    else:
        sys.stdout.write(res_str + '\n')
