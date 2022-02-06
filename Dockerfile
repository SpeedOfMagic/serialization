FROM python:3.9-slim

COPY . .

RUN apt-get update
RUN apt-get -y install protobuf-compiler
RUN pip install -r requirements.txt

COPY ./proto ./src/proto
COPY ./avsc ./src/avsc

RUN protoc --experimental_allow_proto3_optional -I=src/proto --python_out=src/proto --proto_path=src/proto src/proto/objects.proto

CMD python3 src/__main__.py