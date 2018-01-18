from gram2automata import gram2automata
from parsing import *
import re
from itertools import product
import sys


def bfs(rfa, graph, final_pos2nonterm, start_pair, nonterm):
    # start_pair = (rfa_pos, graph_pos)
    smth_changed = False
    pairs_set = {start_pair}
    milled_pairs = set()
    while pairs_set:
        rfa_pos, gr_pos = pairs_set.pop()
        milled_pairs.add((rfa_pos, gr_pos))
        if rfa_pos in final_pos2nonterm and nonterm in final_pos2nonterm[rfa_pos]:
            item = graph[start_pair[1]][gr_pos]
            before_len = len(item)
            item.update(final_pos2nonterm[rfa_pos])
            if before_len < len(item):
                smth_changed = True
        rfa_label2v = defaultdict(set)
        gr_label2v = defaultdict(set)
        gram_out_labels = set()
        graph_out_labels = set()

        for to, label in rfa.transitions.get(rfa_pos, set()):
            gram_out_labels.add(label)
            rfa_label2v[label].add(to)

        for to in graph[gr_pos]:
            for label in graph[gr_pos][to]:
                graph_out_labels.add(label)
                gr_label2v[label].add(to)

        common_labels = gram_out_labels.intersection(graph_out_labels)
        if common_labels:
            pairs_set.update([(new_rfa_pos, new_graph_pos)
                              for label in common_labels
                              for new_rfa_pos, new_graph_pos in product(rfa_label2v[label], gr_label2v[label])
                              if (new_rfa_pos, new_graph_pos) not in milled_pairs
                              ])
    return smth_changed


def bottom_up(rfa, graph):
    ans_set = set()
    gram_states = set()

    for vertex, edges in rfa.transitions.items():
        gram_states.add(vertex)
        for edge in edges:
            gram_states.add(edge[0])

    graph_states = set()
    for fr in graph:
        graph_states.update(set(graph[fr]))
        graph_states.add(fr)

    start_pos2nonterm = defaultdict(set)
    final_pos2nonterm = defaultdict(set)

    for nonterm in rfa.start_states:
        for rfa_state in rfa.start_states[nonterm]:
            start_pos2nonterm[rfa_state].add(nonterm)

    for nonterm in rfa.final_states:
        for rfa_state in rfa.final_states[nonterm]:
            final_pos2nonterm[rfa_state].add(nonterm)

    smth_changed = True
    while smth_changed:
        smth_changed = False
        for gr_pos in graph_states:
            for nonterm in rfa.start_states:
                for rfa_pos in rfa.start_states[nonterm]:
                    smth_changed |= bfs(rfa, graph, final_pos2nonterm, (rfa_pos, gr_pos), nonterm)

    for fr in graph:
        for to in graph[fr]:
                for token in graph[fr][to]:
                    if any(ch.isupper() for ch in token):
                        ans_set.add((fr, token, to))

    return list(ans_set)


if len(sys.argv) > 1:
    res = bottom_up(get_rfa(sys.argv[1]), get_graph(sys.argv[2]))
    res_str = '\n'.join([','.join([str(i), nonterm, str(j)]) for i, nonterm, j in res])
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w') as f:
            f.write(res_str)
            f.close()
    else:
        sys.stdout.write(res_str + '\n')
