import pickle
from objects import ObjectToEvaluate


class Serializer:
    def serialize(self, to_serialize: ObjectToEvaluate) -> bytes:
        raise NotImplementedError('Serializer is an interface and has no implementation')

    def deserialize(self, to_deserialize: bytes) -> ObjectToEvaluate:
        raise NotImplementedError('Serializer is an interface and has no implementation')


class NativeSerializer(Serializer):
    def serialize(self, to_serialize: ObjectToEvaluate) -> bytes:
        return pickle.dumps(to_serialize)

    def deserialize(self, to_deserialize: bytes) -> ObjectToEvaluate:
        return pickle.loads(to_deserialize)
