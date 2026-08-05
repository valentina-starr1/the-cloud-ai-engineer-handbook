"""
Example tracer setup for OpenLLMetry/OpenTelemetry exporting to Jaeger or OTLP.
"""
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import os

def init_tracer(service_name: str = "rag-service"):
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Configure Jaeger exporter if JAEGER_AGENT_HOST set, otherwise OTLP
    jaeger_host = os.environ.get("JAEGER_AGENT_HOST")
    if jaeger_host:
        jaeger_exporter = JaegerExporter(agent_host_name=jaeger_host, agent_port=int(os.environ.get("JAEGER_AGENT_PORT", 6831)))
        provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    else:
        otlp_endpoint = os.environ.get("OTLP_ENDPOINT")
        if otlp_endpoint:
            otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
            provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    return trace.get_tracer(__name__)
