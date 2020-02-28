import random, sys, os
from score import Scorer
from input import parse_input
from parse_tree import ParseTree
from grammar import Grammar, Rule
from generator import GrammarGenerator

def main(file_name, max_iters):
    # Generate configuration options and oracle grammar
    CONFIG, ORACLE_GEN, ORACLE = parse_input(file_name)
    POS_EXAMPLES = CONFIG['POS_EXAMPLES']
    MAX_ITERS = max_iters

    # Generate positive examples
    oracle_parse_tree = ParseTree(ORACLE_GEN)
    positive_examples = oracle_parse_tree.sample_strings(POS_EXAMPLES)
    DATA = {'positive_examples':positive_examples, 'oracle_parser':ORACLE.parser()}

    # Generate intial grammar and score it
    gen = GrammarGenerator(CONFIG)
    grammar = gen.generate_grammar()
    scorer = Scorer(CONFIG, DATA, grammar, gen)
    scorer.score(grammar, gen)

    # Main Program Loop
    iterations = 0
    while iterations < MAX_ITERS:
        good_grammar, good_gen = scorer.sample_grammar()
        new_gen = good_gen.copy()
        new_gen.mutate()
        new_grammar = new_gen.generate_grammar()
        scorer.score(new_grammar, new_gen)
        print('Iters:', iterations, '\tScores:', [v[0] for v in scorer.score_map.values()])
        iterations += 1

    print('\n\n====== RESULTS ======\n\n')
    for category in scorer.score_map:
        score, grammar, gen = scorer.score_map[category]
        print('Category:', category)
        print('Grammar:')
        print(grammar)
        print('Score:', score)
        print()

if __name__ == '__main__':
    if len(sys.argv) != 3 or not os.path.exists(sys.argv[1]):
        print('Usage: python3 generational_search.py <input_file> <max_iters>')
    else:
        try:
            max_iters = int(sys.argv[2])
        except:
            print('Usage: python3 generational_search.py <input_file> <max_iters>')
            exit()
        main(sys.argv[1], max_iters)
