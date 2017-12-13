from string import ascii_uppercase
from itertools import product

class MyGraph:

    def __init__(self, node):
        # nodes is a dict: node -> set((node, label))
        self.nodes = {node: set()}

    def add_node(self, fr, to, label):
        if fr in self.nodes:
            self.nodes[fr].add((to, label))
        else:
            self.nodes[fr] = {(to, label)}


class RFAbox:
    """
    RFA_box has start_state, final_state and dict nodes: int -> set( (int, label) )
    """
    def __init__(self, nonterm, start_state=None, final_state=None):
        self.nodes = {}
        self.nonterm = nonterm
        self.start_state = start_state
        self.final_state = final_state

    def add_node(self, fr, to, label):
        if fr in self.nodes:
            self.nodes[fr].add((to, label))
        else:
            self.nodes[fr] = {(to, label)}


class RFA:

    def __init__(self):
        self.boxes = set()

    def add_box(self, box):
        self.boxes.add(box)

    def get_box_by_nonterminal(self, nonterminal):
        return next(box for box in self.boxes if box.nonterm == nonterminal)


class GLLenv:
    """
    GSS node is a pair (graph_pos, nonterm)
    Configuration is a triple ( graph_pos, (rfa_box_pos, nonterm), gss_node )
    """

    def __init__(self, rfa, graph):
        self.rfa = rfa
        self.graph = graph
        self.popped = set()
        self.milled_confs = set()
        self.ans = set()

    def __add_new_conf__(self, conf):
        if conf not in self.milled_confs:
            self.cur_confs.add(conf)

    def pop_single(self, gss_node, cur_input_state):
        self.ans.add((gss_node[0], gss_node[1], cur_input_state))

    def pop_gss(self, gss_node, cur_input_state):
        trans_set = self.gss.nodes[gss_node]
        res_dict = {}
        for item in trans_set:
            if item[0] in res_dict:
                res_dict[item[0]].append(item[1])
            else:
                res_dict[item[0]] = [item[1]]
        self.popped.add(gss_node)
        self.ans.add((gss_node[0], gss_node[1], cur_input_state))
        return res_dict

    def main(self):
        n = self.graph.shape[0]
        for i in range(n):
            self.gss = MyGraph((i, 'S'))
            self.cur_confs = {(i, (0, 'S'), list(self.gss.nodes)[0])}
            self.milled_confs = set()
            self.popped = set()
            while self.cur_confs:
                self.next_step()
        return list(self.ans)

    def get_from_conf(self, conf):
        return conf[0], conf[1], conf[2]

    def term_trans(self, cur_conf, graph_out_edges, gram_out_edges, box):
        graph_pos, gram_pos, cur_gss_node = self.get_from_conf(cur_conf)
        terminal_intersect = [(gram_edge, graph_edge)
                              for gram_edge, graph_edge in product(gram_out_edges, graph_out_edges)
                              if gram_edge[1] == graph_edge[1]
                              ]

        if terminal_intersect:
            for gram_edge, graph_edge in terminal_intersect:
                    new_conf = (
                        graph_edge[0],
                        (gram_edge[0], box.nonterm),
                        cur_gss_node
                    )
                    self.__add_new_conf__(new_conf)

    def nonterm_calls(self, cur_conf, gram_out_edges, box):
        graph_pos, gram_pos, cur_gss_node = self.get_from_conf(cur_conf)
        nonterm_trans = [(to, nonterm) for to, nonterm in gram_out_edges if nonterm in ascii_uppercase]
        if nonterm_trans:
            for to, nonterm in nonterm_trans:
                new_gss_node = (graph_pos, nonterm)
                new_conf = (
                    graph_pos,
                    (0, nonterm),
                    new_gss_node
                )
                self.__add_new_conf__(new_conf)
                self.gss.add_node(new_gss_node, cur_gss_node, to)
                if new_gss_node in self.popped:
                    self.pop_single(new_gss_node, graph_pos)


    def next_step(self):
        cur_conf = self.cur_confs.pop()
        self.milled_confs.add(cur_conf)
        graph_pos, gram_pos, cur_gss_node = self.get_from_conf(cur_conf)
        cur_box = next(box for box in self.rfa.boxes if box.nonterm == gram_pos[1])

        graph_out_edges = [(to, label) for to, label in enumerate(self.graph[graph_pos]) if label]

        try:
            gram_out_edges = list(cur_box.nodes[gram_pos[0]])

        except KeyError:
            gram_out_edges = []
        # case of common terminals
        self.term_trans(cur_conf, graph_out_edges, gram_out_edges, cur_box)

        # case of calling nonterminal
        self.nonterm_calls(cur_conf, gram_out_edges, cur_box)

        # case of grammar final state
        if gram_pos[0] == 1:
            nonterm_states_dict = self.pop_gss(cur_gss_node, graph_pos)
            for key in nonterm_states_dict:
                for value in nonterm_states_dict[key]:
                    new_conf =(
                        graph_pos,
                        (value, key[1]),
                        key
                    )
                    self.__add_new_conf__(new_conf)