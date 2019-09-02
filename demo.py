import logging
import time

import boto3
import opentracing
from jaeger_client.config import Config
from opentracing_instrumentation.client_hooks.boto3 import install_patches
from opentracing_instrumentation.request_context import span_in_stack_context
from opentracing.scope_managers.tornado import TornadoScopeManager


logging.basicConfig(level=logging.INFO)


BUCKET = 'some-bucket'
FILENAME = 'lorem-ipsum.txt'


def configure_tracing():
    install_patches()
    jaeger_config = Config(
        config={
            'logging': True,
            'sampler': {
                'type': 'const',
                'param': 1,
            },
        },
        scope_manager=TornadoScopeManager(),
        service_name='demo',
    )
    jaeger_config.initialize_tracer()


def upload_file_with_s3_client(bucket, filename):
    s3_client = boto3.client('s3', endpoint_url='http://localhost:4572')
    s3_client.create_bucket(Bucket=bucket)
    s3_client.upload_file(filename, bucket, filename)


def upload_file_with_s3_resource(bucket, filename):
    s3_resource = boto3.resource('s3', endpoint_url='http://localhost:4572')
    s3_resource.create_bucket(Bucket=bucket)
    s3_resource.Object(bucket, filename).upload_file(filename)


if __name__ == '__main__':
    configure_tracing()

    s3_demo_span = opentracing.tracer.start_span(operation_name='s3_demo')
    with s3_demo_span, span_in_stack_context(s3_demo_span):
        span = opentracing.tracer.start_span(
            operation_name='uploading_with_s3_client'
        )
        with span, span_in_stack_context(span):
            upload_file_with_s3_client(BUCKET, FILENAME)

        span = opentracing.tracer.start_span(
            operation_name='uploading_with_s3_resource'
        )
        with span, span_in_stack_context(span):
            upload_file_with_s3_resource(BUCKET, FILENAME)

    # let the tracer push spans to the agent
    time.sleep(3)
