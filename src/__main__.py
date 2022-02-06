from evaluator import Evaluator

if __name__ == '__main__':
    evaluator = Evaluator(num_tests=1000)
    evaluator.evaluate_for_all_pairs()

    for object_name, table in evaluator.tables.items():
        table.to_tsv(object_name + '.tsv')
