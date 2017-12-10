import sys
import threading
import time


class UnitTesting:
    """
    parsing module includes 2 functions:
        get_graph       :: filename -> matrix (np.array)
        get_grammar     :: filename -> grammar (dict :: str -> [str])

    intersection_module includes 1 function:
        lang_intersect  :: grammar, graph-> return list of triples (i, 'S', j)
    """

    def __init__(self, grammar_parsing, graph_parsing, intersection, tests):
        # tests is a dict: (graph_filename, grammar_filename -> true number of triples)
        self.grammar_parsing = grammar_parsing
        self.graph_parsing = graph_parsing
        self.intersection = intersection
        self.tests = tests

    def loading_printing(self):

        def spinning_cursor():
            while True:
                for cursor in '|/-\\':
                    yield cursor

        spinner = spinning_cursor()

        sys.stdout.write('Loading..')
        while not self.exit_event.is_set():
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
        return

    def run_tests(self):

        self.exit_event = threading.Event()

        for test_args in self.tests:
            sys.stdout.write('##############################################\n')
            self.exit_event.clear()
            gram_filename = test_args[0]
            graph_filename = test_args[1]
            true_res = self.tests[test_args]
            sys.stdout.write(str(gram_filename.split('\\')[-1]) + ', ' + str(graph_filename.split('\\')[-1]) + '\n')

            threading.Thread(target=self.loading_printing).start()

            gram = self.grammar_parsing(gram_filename)
            graph = self.graph_parsing(graph_filename)
            my_res = self.intersection(gram, graph)

            if len(my_res) == true_res:
                self.exit_event.set()
                time.sleep(0.1)
                sys.stdout.write('\b..OK!\n')
            else:
                self.exit_event.set()
                time.sleep(0.1)
                sys.stdout.write('\b..Nope :(\n')
            sys.stdout.write('\n\n')