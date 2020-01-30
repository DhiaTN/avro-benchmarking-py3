import json
from io import BytesIO

import avro.io
import avro.schema
import fastavro
import pytest


class TestBenchmark(object):
    @pytest.fixture(scope="session")
    def avro_schema_json(self):
        with open("fixtures/schema.json", "r") as schema:
            return json.loads(schema.read())

    @pytest.fixture(scope="session")
    def avro_encoder(self, avro_schema_json):
        schema = avro.schema.SchemaFromJSONData(avro_schema_json)

        def encoder(message):
            writer = avro.io.DatumWriter(schema)
            writer_stream = BytesIO()
            encoder = avro.io.BinaryEncoder(writer_stream)
            writer.write(message, encoder)
            return writer_stream.getvalue()

        return encoder

    @pytest.fixture(scope="session")
    def avro_decoder(self, avro_schema_json):
        schema = avro.schema.SchemaFromJSONData(avro_schema_json)

        def decoder(encoded_message):
            reader = avro.io.DatumReader(schema)
            reader_stream = BytesIO(encoded_message)
            decoder = avro.io.BinaryDecoder(reader_stream)
            return reader.read(decoder)

        return decoder

    @pytest.fixture
    def fastavro_encoder(self, avro_schema_json):
        def encoder(message):
            writer_stream = BytesIO()
            fastavro.schemaless_writer(writer_stream, avro_schema_json, message)
            return writer_stream.getvalue()

        return encoder

    @pytest.fixture
    def fastavro_decoder(self, avro_schema_json):
        def decoder(encoded_message):
            if not isinstance(encoded_message, bytes):
                raise TypeError
            reader_stream = BytesIO(encoded_message)
            return fastavro.schemaless_reader(reader_stream, avro_schema_json)

        return decoder

    @pytest.fixture(scope="session")
    def record_data(self, avro_schema_json):
        with open("fixtures/record.json", "r") as schema:
            return json.loads(schema.read())

    @pytest.fixture(scope="session")
    def record_binary(self, avro_encoder, record_data):
        return avro_encoder(record_data)

    @pytest.fixture(params=["avro_encoder", "fastavro_encoder"])
    def encoder(self, request):
        return request.getfixturevalue(request.param)

    @pytest.fixture(params=["avro_decoder", "fastavro_decoder"])
    def decoder(self, request):
        return request.getfixturevalue(request.param)

    @pytest.mark.benchmark(group="Encoders",)
    def test_avro_encoder(self, benchmark, encoder, record_data):
        benchmark.pedantic(
            target=encoder,
            args=[record_data],
            iterations=10,
            rounds=10000,
            warmup_rounds=100,
        )

    @pytest.mark.benchmark(group="Decoders",)
    def test_decoder(self, benchmark, decoder, record_binary):
        benchmark.pedantic(
            target=decoder,
            args=[record_binary],
            iterations=10,
            rounds=10000,
            warmup_rounds=100,
        )
