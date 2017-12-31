from parsing import *
import re
from itertools import product
import sys

def traversal(graph, rfa, nonterm, final_set, used_edges):
    # used edges - list of pairs (graph_pos, rfa_pos) if we wanna add an existing edge - interrupt traversal
    graph_pos, rfa_pos = used_edges[-1]
    if rfa_pos in final_set:
        fr = used_edges[0][0]
        to = used_edges[-1][0]
        graph[fr, to].add(nonterm)

    gram_out_edges = rfa.transitions.get(rfa_pos, [])

    graph_out_edges = [(to, label_set) for to, label_set in enumerate(graph[graph_pos]) if label_set]

    for gram_edge, graph_edge in product(gram_out_edges, graph_out_edges):
        if gram_edge[1] in graph_edge[1]:
            new_conf = (graph_edge[0], gram_edge[0])
            if not new_conf in used_edges:
                new_used = used_edges.copy()
                new_used.append(new_conf)
                traversal(graph, rfa, nonterm, final_set, new_used)


def bottom_up(rfa, matrix):
    n = matrix.shape[0]
    gram_states = set()

    nonterm_str_regex = re.compile(
        r"[A-Z]+"
    )

    for vertex, edges in rfa.transitions.items():
        gram_states.add(vertex)
        for edge in edges:
            gram_states.add(edge[0])

    closed_graph = np.vectorize(set)(matrix)
    res_set = set()

    while True:
        len_before = len(res_set)
        for nonterm in rfa.key_states:
            final_states = rfa.key_states[nonterm]['final']
            for start_state in rfa.key_states[nonterm]['start']:
                for graph_state in range(n):
                    traversal(closed_graph, rfa, nonterm, final_states, used_edges=[(graph_state, start_state)])
        res_set = set((i, symbol, j) for i, j in product(range(n), repeat=2) for symbol in closed_graph[i,j]
                    if nonterm_str_regex.search(symbol))
        len_after = len(res_set)
        if len_before < len_after:
            continue
        else:
            break

    return list(res_set)


if len(sys.argv) > 1:
    res = bottom_up(get_rfa(sys.argv[1]), get_graph(sys.argv[2]))
    res_str = '\n'.join([','.join([str(i), nonterm, str(j)]) for i, nonterm, j in res])
    if len(sys.argv) > 3:
        with open(sys.argv[3]) as f:
            f.write(res_str)
            f.close()
    else:
        sys.stdout.write(res_str + '\n')
