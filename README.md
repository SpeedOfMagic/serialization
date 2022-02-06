# Serialization profiler

This application allows you to profile serialization algorithms. For each object it serializes and deserializes it, then it measures used memory and time used to perform both operations.

## Used objects:
- PrimitiveObject, lightweight object with two ints and two floats
- DictObject, medium object with three dicts
- RepeatedObject, heavy object with two strings and two arrays. All fields have big size.
- CompositeObject

## Used serializers:
- Native serializer for Python (pickle)
- XML serializer (xmltodict)
- JSON serializer (json)
- Proto serializer (proto)
- Avro serializer (fastavro)
- YAML serializer (pyyaml)
- MessagePack serializer (msgpack)
