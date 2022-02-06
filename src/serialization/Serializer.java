package serialization;

import objects.Evaluatable;

public interface Serializer {
    void SerializeToFile(Evaluatable objectToEvaluate, String filePath);
    Evaluatable DeserializeFromFile(String filePath);
}
