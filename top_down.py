from parsing import *
from gss.gss_classes import *
import sys

def gram2automata(gram):
    rfa = RFA()
    for nonterm in gram:
        box = RFAbox(nonterm, start_state=0)
        cur_id = 2
        for production in gram[nonterm]:
            if len(production) == 1:
                box.add_node(0, 1, production)
                continue

            box.add_node(0, cur_id, production[0])

            for ch in production[1:-1]:
                box.add_node(cur_id, cur_id + 1, ch)
                cur_id += 1

            box.add_node(cur_id, 1, production[-1])
            cur_id += 1
        rfa.add_box(box)
    return rfa


def top_down(gram, matrix):
    gram = {k: [prod.replace(' ', '') for prod in v] for k, v in gram.items()}
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