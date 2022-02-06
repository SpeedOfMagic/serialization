import pickle
import json
import fastavro
import fastavro.schema
import xmltodict
import yaml
import msgpack

from objects import ObjectToEvaluate


class Serializer:
    def serialize(self, to_serialize: ObjectToEvaluate) -> bytes:
        raise NotImplementedError("serialize is not defined!")

    def deserialize(self, to_deserialize: bytes) -> ObjectToEvaluate:
        raise NotImplementedError("deserialize is not defined!")


class Native(Serializer):
    def serialize(self, to_serialize: ObjectToEvaluate) -> bytes:
        return pickle.dumps(to_serialize)

    def deserialize(self, to_deserialize: bytes) -> ObjectToEvaluate:
        return pickle.loads(to_deserialize)


class XML(Serializer):
    def __init__(self):
        self.obj_class = None

    def serialize(self, to_serialize: ObjectToEvaluate) -> str:
        self.obj_class = to_serialize.__class__
        return xmltodict.unparse({"root": vars(to_serialize)}, short_empty_elements=True)

    def deserialize(self, to_deserialize: str) -> ObjectToEvaluate:
        kwargs = dict(xmltodict.parse(to_deserialize, xml_attribs=False)["root"])
        return self.obj_class(**kwargs)


class JSON(Serializer):
    def __init__(self):
        self.obj_class = None

    def serialize(self, to_serialize: ObjectToEvaluate) -> str:
        self.obj_class = to_serialize.__class__
        return json.dumps(vars(to_serialize))

    def deserialize(self, to_deserialize: str) -> ObjectToEvaluate:
        return self.obj_class(**json.loads(to_deserialize))


class Proto(Serializer):
    def __init__(self):
        self.obj_class = None

    def serialize(self, to_serialize: ObjectToEvaluate) -> str:
        self.obj_class = to_serialize.__class__
        return to_serialize.map_to_protobuf()

    def deserialize(self, to_deserialize: bytes) -> ObjectToEvaluate:
        return self.obj_class.from_protobuf(to_deserialize)


class Avro(Serializer):
    def __init__(self):
        self.obj_class = None
        self.parsed_schema = None

    def serialize(self, to_serialize: ObjectToEvaluate) -> bytes:
        self.obj_class = to_serialize.__class__

        if self.parsed_schema is None:
            schema_file = "avsc/" + to_serialize.__class__.__name__ + ".avsc"
            self.parsed_schema = fastavro.schema.load_schema(schema_file)

        with open("tmp.avro", "wb") as out:
            fastavro.writer(out, self.parsed_schema, [vars(to_serialize)])
        return open("tmp.avro", "rb").read()

    def deserialize(self, to_deserialize: bytes) -> ObjectToEvaluate:
        self.parsed_schema = None
        with open("tmp.avro", "rb") as serialized:
            result = None
            for obj in fastavro.reader(serialized):
                result = obj
            return self.obj_class(**dict(result))


class Yaml(Serializer):
    def serialize(self, to_serialize: ObjectToEvaluate) -> bytes:
        return yaml.dump(to_serialize, Dumper=yaml.CDumper)

    def deserialize(self, to_deserialize: bytes) -> ObjectToEvaluate:
        return yaml.load(to_deserialize, Loader=yaml.CLoader)


class MessagePack(Serializer):
    def __init__(self):
        self.obj_class = None

    def serialize(self, to_serialize: ObjectToEvaluate) -> bytes:
        self.obj_class = to_serialize.__class__
        return msgpack.packb(vars(to_serialize))

    def deserialize(self, to_deserialize: bytes) -> ObjectToEvaluate:
        return self.obj_class(**msgpack.unpackb(to_deserialize))
