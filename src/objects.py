class ObjectToEvaluate:
    pass


class TestObject(ObjectToEvaluate):
    def __init__(self, a=2, b=3.14, c="cde"):
        self.a = a
        self.b = b
        self.c = c
