import proto.objects_pb2


class ObjectToEvaluate:
    def map_to_protobuf(self):
        raise NotImplementedError("map_to_protobuf is not defined!")

    @staticmethod
    def from_protobuf(protobuf_str: str):
        raise NotImplementedError("from_protobuf is not defined!")

    def __eq__(self, other):
        raise NotImplementedError("== is not defined!")


class PrimitiveObject(ObjectToEvaluate):
    def __init__(self, int1: int, float1: float, int2: int, float2: float):
        self.int1 = int(int1)
        self.float1 = float(float1)
        self.int2 = int(int2)
        self.float2 = float(float2)

    def __eq__(self, other):
        return self.int1 == other.int1 and self.int2 == other.int2 \
            and abs(self.float1 - other.float1) / max(self.float1, other.float1) < 10 ** (-9) \
            and abs(self.float2 - other.float2) / max(self.float2, other.float2) < 10 ** (-9)

    def map_to_protobuf(self) -> str:
        protobuf = proto.objects_pb2.PrimitiveObject(**vars(self))
        return protobuf.SerializeToString()

    @staticmethod
    def from_protobuf(protobuf_str: str) -> ObjectToEvaluate:
        proto_object = proto.objects_pb2.PrimitiveObject.FromString(protobuf_str)
        return PrimitiveObject(int1=proto_object.int1, float1=proto_object.float1,
                               int2=proto_object.int2, float2=proto_object.float2)


class RepeatedObject(ObjectToEvaluate):
    def __init__(self, str1: str, str2: str, arr1: list[int], arr2: list[str]):
        self.str1 = str1
        self.str2 = str2
        self.arr1 = list(map(int, arr1))
        self.arr2 = arr2

    def __eq__(self, other):
        return self.str1 == other.str1 and self.str2 == other.str2 \
            and self.arr1 == other.arr1 and self.arr2 == other.arr2

    def map_to_protobuf(self) -> str:
        protobuf = proto.objects_pb2.RepeatedObject(**vars(self))
        return protobuf.SerializeToString()

    @staticmethod
    def from_protobuf(protobuf_str: str) -> ObjectToEvaluate:
        proto_object = proto.objects_pb2.RepeatedObject.FromString(protobuf_str)
        return RepeatedObject(str1=proto_object.str1, str2=proto_object.str2,
                              arr1=proto_object.arr1, arr2=proto_object.arr2)


class DictObject(ObjectToEvaluate):
    def __init__(self, dict1: dict[str, int], dict2: dict[str, int], dict3: dict[str, str]):
        self.dict1 = {k: int(v) for k, v in dict(dict1).items()}
        self.dict2 = {k: int(v) for k, v in dict(dict2).items()}
        self.dict3 = dict(dict3)

    def __eq__(self, other):
        return self.dict1 == other.dict1 and self.dict2 == other.dict2 and self.dict3 == other.dict3

    def map_to_protobuf(self) -> str:
        protobuf = proto.objects_pb2.DictObject(**vars(self))
        return protobuf.SerializeToString()

    @staticmethod
    def from_protobuf(protobuf_str: str) -> ObjectToEvaluate:
        proto_object = proto.objects_pb2.DictObject.FromString(protobuf_str)
        return DictObject(dict1=proto_object.dict1, dict2=proto_object.dict2, dict3=proto_object.dict3)


class CompositeObject(ObjectToEvaluate):
    def __init__(self, int1: int, float1: float, str1: str, arr1: list[int], dict1: dict[str, list[str]]):
        self.int1 = int(int1)
        self.float1 = float(float1)
        self.str1 = str1
        self.arr1 = list(map(int, arr1))
        self.dict1 = dict(dict1)

    def __eq__(self, other):
        return self.int1 == other.int1 and self.str1 == other.str1 \
            and abs(self.float1 - other.float1) / max(self.float1, other.float1) < 10 ** (-9)\
            and self.arr1 == other.arr1 and self.dict1 == other.dict1

    def map_to_protobuf(self) -> str:
        protobuf = proto.objects_pb2.CompositeObject(**vars(self))
        return protobuf.SerializeToString()

    @staticmethod
    def from_protobuf(protobuf_str: str) -> ObjectToEvaluate:
        proto_object = proto.objects_pb2.CompositeObject.FromString(protobuf_str)
        return CompositeObject(int1=proto_object.int1, float1=proto_object.float1, str1=proto_object.str1,
                               arr1=proto_object.arr1, dict1=proto_object.dict1)
