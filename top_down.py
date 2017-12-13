from parsing import *
from gss.gss_classes import *
import sys
from gram2automata import gram2automata


def top_down(gram, matrix):
    gram = {k: [prod for prod in v] for k, v in gram.items()}
    gll = GLLenv(gram2automata(gram), matrix)
    return gll.main()

if len(sys.argv) > 1:
    res = top_down(get_grammar(sys.argv[1]), get_graph(sys.argv[2]))
    res_str = '\n'.join([','.join([str(i), nonterm, str(j)]) for i, nonterm, j in res])
    if len(sys.argv) > 3:
        with open(sys.argv[3]) as f:
            f.write(res_str)
            f.close()
    else:
        sys.stdout.write(res_str + '\n')