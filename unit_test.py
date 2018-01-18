from gram2automata import gram2automata
from unit_testing.unittest_class import UnitTesting
from parsing import *
from matrix_method import *
from top_down import top_down
from bottom_up import bottom_up


def my_test_gen(mod_name):
    graphs = map(lambda x: 'my_data/inputs/' + x + '.dot', [
        'aaaaa',
        'mutual_loop',
        'my_in_1',
        'my_in_2',
        'my_in_3',
        'rand_1'
    ])

    if mod_name == 'm':
        grammars = map(lambda x: 'my_data/grammars/' + x + '.gr', ['My_1', 'My_2'])
        ans = [0, 20, 2, 3, 3, 77655, 15, 16, 2, 3, 3, 3095]
    else:
        grammars = map(lambda x: 'my_data/grammars/' + x + '.dot', ['an_bn', 'a_star_b', 'some_rfa_1'])
        ans = [6, 27, 3, 5, 7, 1995, 0, 8, 2, 4, 6, 3074, 5, 5, 3, 5, 5, 9507]

    return dict(zip(product(grammars, graphs), ans))

def semen_test_gen(mod_name):

    if mod_name == 'm':
        grammars = map(lambda x: 'data/' + x + '.gr', ['Q1', 'Q2'])
    else:
        grammars = map(lambda x: 'data/' + x + '.gr', ['Q1_', 'Q2_'])

    graphs = map(lambda x: 'data/' + x + '.dot', [
        'skos',
        'generations',
        'travel',
        'univ-bench',
        'atom-primitive',
        'biomedical-measure-primitive',
        'foaf',
        'people-pets',
        'funding',
        'wine',
        'pizza'
    ])

    ans = [810, 2164, 2499, 2540, 15454, 15156, 4118, 9472, 17634, 66572, 56195, 1, 0, 63, 81, 122, 2871, 10, 37, 1158,
    133, 1262]

    return dict(zip(product(grammars, graphs), ans))

while True:
    test_type = input( '\n' +
        """If u wanna run tests:
         from google doc (for Q1 and Q2 grammars): print '1'
         my tests, which are located in the folder my_data: print '2'""" + '\n'
    )
    if test_type != '1' and test_type != '2':
        print('Wrong input, try again\n')
    else: break

while True:
    module_name = input(
        '\n' + """If u wanna run tests for:
                matrix module: print 'm'
                top-down module: print 't'
                bottom-up module: print 'b'""" + '\n')
    if module_name != 'm' and module_name != 'b' and module_name != 't':
        print('Wrong input, try again\n')
    else: break


modules = {
    'm': grammar_closure,
    't': top_down,
    'b': bottom_up
}

if test_type == '1':
    tests = semen_test_gen(module_name)

    if module_name == 't' or module_name == 'b':
        ut = UnitTesting(lambda x: gram2automata(get_grammar(x)), get_graph, modules[module_name], tests)
        ut.run_tests()
    else:
        ut = UnitTesting(get_grammar, get_graph, modules[module_name], tests)
        ut.run_tests()

if test_type == '2':
    tests = my_test_gen(module_name)

    if module_name == 't' or module_name == 'b':
        ut = UnitTesting(get_rfa, get_graph, modules[module_name], tests)
        ut.run_tests()
    else:
        ut = UnitTesting(get_grammar, get_graph, modules[module_name], tests)
        ut.run_tests()