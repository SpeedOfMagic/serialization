from evaluator import Evaluator

if __name__ == '__main__':
    evaluator = Evaluator(num_tests=1000)
    evaluator.evaluate_for_all_pairs()

    evaluator.data_size.to_tsv('serialized_data_size.tsv')
    evaluator.serialization_time.to_tsv('serialization_time.tsv')
    evaluator.deserialization_time.to_tsv('deserialization_time.tsv')
    evaluator.total_time.to_tsv('total_time.tsv')
