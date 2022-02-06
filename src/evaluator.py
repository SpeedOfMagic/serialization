import timeit

from objects import *
from serializers import *
from table import Table


class Evaluator:
    OBJECTS_TO_EVALUATE = (
        TestObject(),
    )

    SERIALIZERS_TO_EVALUATE = (
        NativeSerializer(),
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

    def _evaluate_for(self, object_to_evaluate: ObjectToEvaluate, serializer: Serializer) -> None:
        used_time_to_serialize = timeit.timeit(
            stmt='serializer.serialize(object_to_evaluate)',
            number=self.num_tests,
            globals=locals()
        )
        self.serialization_time.set(used_time_to_serialize)

        serialized = serializer.serialize(object_to_evaluate)
        self.data_size.set(len(serialized))

        used_time_to_deserialize = timeit.timeit(
            stmt='serializer.deserialize(serialized)',
            number=self.num_tests,
            globals=locals()
        )
        self.deserialization_time.set(used_time_to_deserialize)

        self.total_time.set(used_time_to_serialize + used_time_to_deserialize)

    def evaluate_for_all_pairs(self):
        for object_to_evaluate in self.OBJECTS_TO_EVALUATE:
            for serializer in self.SERIALIZERS_TO_EVALUATE:
                self._evaluate_for(object_to_evaluate, serializer)
