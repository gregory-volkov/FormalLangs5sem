from gss.gss_classes import RFA, RFAbox


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