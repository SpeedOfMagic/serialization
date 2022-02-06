import timeit

from objects import *
from serializers import *
from table import Table


class Evaluator:
    OBJECTS_TO_EVALUATE = (
        PrimitiveObject(int1=9, float1=3.1415, int2=-5156, float2=1e128),
        RepeatedObject(str1="lorem ipsum." * 100, str2="a", arr1=[1, 2, 3, 5], arr2=["Hello world!"] * 255),
    )

    SERIALIZERS_TO_EVALUATE = (
        NativeSerializer(),
        XMLSerializer(),
    )

    INDEX = list(map(lambda obj: obj.__class__.__name__, OBJECTS_TO_EVALUATE))
    COLUMNS = list(map(lambda obj: obj.__class__.__name__, SERIALIZERS_TO_EVALUATE))

    num_tests: int
    data_size: Table
    serialization_time: Table
    deserialization_time: Table
    total_time: Table

    def __init__(self, num_tests: int = 1000):
        self.num_tests = num_tests
        self.data_size = Table(self.INDEX, self.COLUMNS)
        self.serialization_time = Table(self.INDEX, self.COLUMNS)
        self.deserialization_time = Table(self.INDEX, self.COLUMNS)
        self.total_time = Table(self.INDEX, self.COLUMNS)

    def _evaluate_for(self, obj: ObjectToEvaluate, serializer: Serializer) -> None:
        used_time_to_serialize = timeit.timeit(
            stmt='serializer.serialize(obj)',
            number=self.num_tests,
            globals=locals()
        )
        self.serialization_time.set(used_time_to_serialize)

        serialized = serializer.serialize(obj)
        self.data_size.set(len(serialized))

        used_time_to_deserialize = timeit.timeit(
            stmt='serializer.deserialize(serialized)',
            number=self.num_tests,
            globals=locals()
        )
        self.deserialization_time.set(used_time_to_deserialize)
        
        deserialized = serializer.deserialize(serialized)
        assert deserialized == obj, \
            f'Serializer {serializer.__class__.__name__} returned wrong value for object {obj.__class__.__name__}'

        self.total_time.set(used_time_to_serialize + used_time_to_deserialize)
        print('Done')

    def evaluate_for_all_pairs(self):
        for obj in self.OBJECTS_TO_EVALUATE:
            for serializer in self.SERIALIZERS_TO_EVALUATE:
                self._evaluate_for(obj, serializer)
