class ObjectToEvaluate:
    def __eq__(self, other):
        raise NotImplementedError('== is not defined!')


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


class RepeatedObject(ObjectToEvaluate):
    def __init__(self, str1: str, str2: str, arr1: list[int], arr2: list[str]):
        self.str1 = str1
        self.str2 = str2
        self.arr1 = list(map(int, arr1))
        self.arr2 = arr2

    def __eq__(self, other):
        return self.str1 == other.str1 and self.str2 == other.str2 \
            and self.arr1 == other.arr1 and self.arr2 == other.arr2