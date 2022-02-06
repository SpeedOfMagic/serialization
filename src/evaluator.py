import timeit
import os

from objects import *
from serializers import *
from table import Table


class Evaluator:
    OBJECTS_TO_EVALUATE = (
        PrimitiveObject(int1=9, float1=3.1415, int2=-5156, float2=1e128),  # Light object
        DictObject(dict1={"D" + str(i): i ** 2 for i in range(100)},  # Medium object
                   dict2={"a": -123456789},
                   dict3={s: s + s + s for s in ["a", "b", "c", "d", "e", "f"]}),
        RepeatedObject(str1="lorem ipsum." * 100,  # Heavy object
                       str2="a" * 1000,
                       arr1=[1, 2, 3, 5],
                       arr2=["Hello world!"] * 255),
        CompositeObject(int1=123456789987654321, float1=0.0001,  # Very heavy object
                        str1="Some more of an exciting and interesting text!" * 1000,
                        arr1=list(range(500)),
                        dict1={"INT" + str(i): str(i) * 100 for i in range(100)})
    )

    SERIALIZERS_TO_EVALUATE = (
        NativeSerializer(),
        XMLSerializer(),
        JSONSerializer(),
        ProtoSerializer(),
        AvroSerializer(),
        YamlSerializer(),
        MessagePackSerializer(),
    )

    INDEX = list(map(lambda obj: obj.__class__.__name__, SERIALIZERS_TO_EVALUATE))
    COLUMNS = ['data_size', 'serialization_time', 'deserialization_time', 'total_time']

    num_tests: int
    tables: dict[str, Table]

    def __init__(self, num_tests):
        self.num_tests = num_tests
        self.tables = {obj.__class__.__name__: Table(self.INDEX, self.COLUMNS) for obj in self.OBJECTS_TO_EVALUATE}

    def _evaluate_for(self, obj: ObjectToEvaluate, serializer: Serializer) -> None:
        print(f"Measuring time for object {obj.__class__.__name__} with serializer {serializer.__class__.__name__}")
        used_time_to_serialize = timeit.timeit(
            stmt="serializer.serialize(obj)",
            number=self.num_tests,
            globals=locals()
        )
        used_time_to_serialize = round(used_time_to_serialize, 6)

        serialized = serializer.serialize(obj)

        used_time_to_deserialize = timeit.timeit(
            stmt="serializer.deserialize(serialized)",
            number=self.num_tests,
            globals=locals()
        )
        used_time_to_deserialize = round(used_time_to_deserialize, 6)

        deserialized = serializer.deserialize(serialized)
        assert deserialized == obj, \
            f"Serializer {serializer.__class__.__name__} returned wrong value for object {obj.__class__.__name__}"

        total_time = round(used_time_to_serialize + used_time_to_deserialize, 6)

        self.tables[obj.__class__.__name__].set(len(serialized))
        self.tables[obj.__class__.__name__].set(used_time_to_serialize)
        self.tables[obj.__class__.__name__].set(used_time_to_deserialize)
        self.tables[obj.__class__.__name__].set(total_time)

        print("RESULTS:")
        print("Total size (in bytes):", len(serialized))
        print("Serialization time:", used_time_to_serialize, "s")
        print("Deserialization time:", used_time_to_deserialize, "s")
        print("Total time:", total_time, "s")
        print("Done")

    def evaluate_for_all_pairs(self):
        for obj in self.OBJECTS_TO_EVALUATE:
            for serializer in self.SERIALIZERS_TO_EVALUATE:
                self._evaluate_for(obj, serializer)
        if os.path.exists("tmp.avro"):
            os.remove("tmp.avro")
