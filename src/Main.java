public class Main {
    public static void main(String[] args) {
        Evaluator evaluator = new Evaluator("tmp.dat");
        evaluator.EvaluateForAllPairs();
        
        evaluator.usedMemory.toTsv("size_of_serialized_file.tsv");
        evaluator.serializationTime.toTsv("serialization_time.tsv");
        evaluator.deserializationTime.toTsv("deserialization_time.tsv");
        evaluator.totalTime.toTsv("total_time.tsv");
    }
}