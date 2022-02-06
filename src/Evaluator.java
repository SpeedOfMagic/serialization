import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;

import serialization.LanguageSerializer;
import serialization.Serializer;
import objects.Evaluatable;
import objects.TestObjMain;


public final class Evaluator {
    private static final List<? extends Evaluatable> OBJECTS_TO_EVALUATE = List.of(
        new TestObjMain()
    );

    private static final List<? extends Serializer> SERIALIZERS_TO_EVALUATE = List.of(
        new LanguageSerializer()
    );

    private String tmpFileName;

    private static final List<String> INDEX = OBJECTS_TO_EVALUATE
        .stream()
        .map(obj -> obj.getClass().getSimpleName())
        .collect(Collectors.toList());
        
    private static final List<String> COLUMNS = SERIALIZERS_TO_EVALUATE
        .stream()
        .map(obj -> obj.getClass().getSimpleName())
        .collect(Collectors.toList());

    public Table usedMemory = new Table("Size of serialized file", INDEX, COLUMNS);
    public Table serializationTime = new Table("Serialization time", INDEX, COLUMNS);
    public Table deserializationTime = new Table("Deserialization time", INDEX, COLUMNS);
    public Table totalTime = new Table("Total time", INDEX, COLUMNS);

    Evaluator(String tmpFileName) {
        this.tmpFileName = tmpFileName;
    }

    void EvaluateFor(Evaluatable objectToEvaluate, Serializer serializer) {
        long start = System.currentTimeMillis();
        serializer.SerializeToFile(objectToEvaluate, tmpFileName);
        long stop = System.currentTimeMillis();

        long usedTimeToSerialize = stop - start;
        serializationTime.set(usedTimeToSerialize);

        try {
            usedMemory.set(Files.size(Paths.get(tmpFileName)));
        } catch (IOException e) {
            System.err.println("IOException has occured while getting file size of " + tmpFileName);
            e.printStackTrace();
            System.exit(1);
        }

        start = System.currentTimeMillis();
        serializer.DeserializeFromFile(tmpFileName);
        stop = System.currentTimeMillis();

        long usedTimeToDeserialize = stop - start;
        deserializationTime.set(usedTimeToDeserialize);
        totalTime.set(usedTimeToSerialize + usedTimeToDeserialize);

        new File(tmpFileName).delete();
    }

    void EvaluateForAllPairs() { 
        for (Evaluatable objectToEvaluate : OBJECTS_TO_EVALUATE) {
            for (Serializer serializer : SERIALIZERS_TO_EVALUATE) {
                EvaluateFor(objectToEvaluate, serializer);
            }
        }
    }
}
