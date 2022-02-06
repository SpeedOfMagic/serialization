import pickle
import xmltodict
import json

from objects import ObjectToEvaluate


class Serializer:
    def serialize(self, to_serialize: ObjectToEvaluate) -> bytes:
        raise NotImplementedError('serialize is not defined!')

    def deserialize(self, to_deserialize: bytes) -> ObjectToEvaluate:
        raise NotImplementedError('deserialize is not defined!')


class NativeSerializer(Serializer):
    def serialize(self, to_serialize: ObjectToEvaluate) -> bytes:
        return pickle.dumps(to_serialize)

    def deserialize(self, to_deserialize: bytes) -> ObjectToEvaluate:
        return pickle.loads(to_deserialize)


class XMLSerializer(Serializer):
    def __init__(self):
        self.obj_class = None

    def serialize(self, to_serialize: ObjectToEvaluate) -> str:
        self.obj_class = to_serialize.__class__
        return xmltodict.unparse({'root': vars(to_serialize)}, short_empty_elements=True)

    def deserialize(self, to_deserialize: str) -> ObjectToEvaluate:
        kwargs = dict(xmltodict.parse(to_deserialize, xml_attribs=False)['root'])
        return self.obj_class(**kwargs)


class JSONSerializer(Serializer):
    def __init__(self):
        self.obj_class = None

    def serialize(self, to_serialize: ObjectToEvaluate) -> str:
        self.obj_class = to_serialize.__class__
        return json.dumps(vars(to_serialize))

    def deserialize(self, to_deserialize: str) -> ObjectToEvaluate:
        return self.obj_class(**json.loads(to_deserialize))
