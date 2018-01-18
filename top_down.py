from parsing import *
import sys
from gss.gll import *
from gram2automata import gram2automata


def top_down(rfa, matrix):
    gll = GLL(rfa, matrix)
    return gll.main()

if len(sys.argv) > 1:
    res = top_down(get_rfa(sys.argv[1]), get_graph(sys.argv[2]))
    res_str = '\n'.join([','.join([str(i), nonterm, str(j)]) for i, nonterm, j in res])
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w') as f:
            f.write(res_str)
            f.close()
    else:
        sys.stdout.write(res_str + '\n')
