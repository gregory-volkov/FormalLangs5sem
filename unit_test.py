from unit_testing.unittest_class import UnitTesting
from parsing import *
from matrix_method import *
from top_down import top_down
from bottom_up import bottom_up

def test_gen(mod_name):

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


module_name = input(
    '\n' + """If u wanna run unit tests for:
            matrix module: print 'm'
            top-down module: print 't'
            bottom-up module: print 'b'""" + '\n')

modules = {
    'm': grammar_closure,
    't': top_down,
    'b': bottom_up
}

tests = test_gen(module_name)


if module_name in modules:
    ut = UnitTesting(get_grammar, get_graph, modules[module_name], tests)
    ut.run_tests()
else:
    print('Wrong module name')