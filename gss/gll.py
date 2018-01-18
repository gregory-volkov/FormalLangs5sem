from collections import defaultdict
from string import ascii_uppercase, digits
from itertools import product


class MyGraph:

    def __init__(self, node):
        # nodes is a dict: node -> set((node, label))
        self.nodes = defaultdict(set)
        self.nodes = {node: set()}

    def add_node(self, fr, to, label):
        if fr in self.nodes:
            self.nodes[fr].add((to, label))
        else:
            self.nodes[fr] = {(to, label)}


class RFA:

    def __init__(self, start_states, final_states, transitions):
        # start_states and final_states are dicts: nonterm -> set(state)
        # transitions : vertex -> set((vertex, label))
        self.start_states = start_states
        self.transitions = transitions
        self.final_states = final_states


class GLL:
    """
    GSS node is a pair (graph_pos, nonterm)
    Configuration is a triple ( graph_pos, rfa_pos, gss_node )
    """

    def __init__(self, rfa, graph):
        self.rfa = rfa
        self.graph = graph
        self.is_nonterm = lambda v: any(char in ascii_uppercase for char in v)

        # set of popped gss nodes
        self.popped = set()

        # set of "utilized" configurations
        self.milled_confs = set()

        # set of answer-triples (i, nonterm, j)
        self.ans = set()

        # dict of the type gss_node -> set of input positions, where the gss_node was popped
        self.popped_states = defaultdict(set)

    def __add_new_conf__(self, conf):
        if conf not in self.milled_confs:
            self.cur_confs.add(conf)

    def pop_gss(self, gss_node, cur_input_state):
        trans_set = self.gss.nodes[gss_node]
        self.popped_states[gss_node].add(cur_input_state)
        for node, label in trans_set:
            for graph_pos in self.popped_states[gss_node]:
                new_conf = (
                    graph_pos,
                    label,
                    node
                )
                self.__add_new_conf__(new_conf)
        self.ans.add((gss_node[0], gss_node[1], cur_input_state))
        self.popped.add(gss_node)

    def pop_single(self, popped_node, cur_node, label):
        for graph_pos in self.popped_states[popped_node]:
            new_conf = (
                graph_pos,
                label,
                cur_node
            )
            self.__add_new_conf__(new_conf)

    def main(self):
        rfa_start_positions = set()
        graph_start_positions = set()

        for nonterm in self.rfa.start_states:
            for rfa_pos in self.rfa.start_states[nonterm]:
                rfa_start_positions.add((nonterm, rfa_pos))

        for fr in self.graph:
            graph_start_positions.update(set(self.graph[fr]))
            graph_start_positions.add(fr)


        for graph_pos in graph_start_positions:
            for nonterm, start_state in rfa_start_positions:
                self.gss = MyGraph((graph_pos, nonterm))
                self.cur_confs = {(graph_pos, start_state, (graph_pos, nonterm))}
                self.milled_confs = set()
                self.popped = set()
                self.popped_states = defaultdict(set)
                while self.cur_confs:
                    self.next_step()
        return list(self.ans)

    def term_trans(self, cur_conf, graph_out_edges, gram_out_edges):
        graph_pos, gram_pos, cur_gss_node = cur_conf

        terminal_intersect = [(gram_edge, graph_edge)
                              for gram_edge, graph_edge in product(gram_out_edges, graph_out_edges)
                              if gram_edge[1] == graph_edge[1]
                              ]
        if terminal_intersect:
            for gram_edge, graph_edge in terminal_intersect:
                    new_conf = (
                        graph_edge[0],
                        gram_edge[0],
                        cur_gss_node
                    )
                    self.__add_new_conf__(new_conf)

    def nonterm_calls(self, cur_conf, gram_out_edges):
        graph_pos, gram_pos, cur_gss_node = cur_conf

        nonterm_trans = [(to, nonterm) for to, nonterm in gram_out_edges if self.is_nonterm(nonterm)]

        if nonterm_trans:
            for label, nonterm in nonterm_trans:
                for start_pos in self.rfa.start_states[nonterm]:
                    new_gss_node = (graph_pos, nonterm)

                    new_conf = (
                        graph_pos,
                        start_pos,
                        new_gss_node
                    )

                    if new_gss_node in self.popped:
                        self.pop_single(new_gss_node, cur_gss_node, label)
                    self.__add_new_conf__(new_conf)
                    self.gss.add_node(new_gss_node, cur_gss_node, label)

    def nonterm_final_state(self, cur_conf):
        graph_pos, gram_pos, cur_gss_node = cur_conf
        if gram_pos in self.rfa.final_states[cur_gss_node[1]]:
            self.pop_gss(cur_gss_node, graph_pos)
            self.popped.add(cur_gss_node)

    def next_step(self):
        cur_conf = self.cur_confs.pop()
        self.milled_confs.add(cur_conf)
        graph_pos, gram_pos, cur_gss_node = cur_conf

        graph_out_edges = [(to, label) for to in self.graph[graph_pos] for label in self.graph[graph_pos][to]]

        if gram_pos in self.rfa.transitions:
            gram_out_edges = self.rfa.transitions[gram_pos]
        else:
            gram_out_edges = []

        # case of common terminals
        self.term_trans(cur_conf, graph_out_edges, gram_out_edges)

        # case of calling nonterminal
        self.nonterm_calls(cur_conf, gram_out_edges)

        # case of grammar final state
        self.nonterm_final_state(cur_conf)
