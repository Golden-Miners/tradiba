from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

_tracer_configured = False


def setup_tracing(service_name: str = "tradiba") -> None:
    global _tracer_configured
    if _tracer_configured:
        return
        
    provider = TracerProvider()
    
    # In production, you would use OTLPExporter to send traces to Jaeger or Tempo.
    # We use ConsoleSpanExporter for local debugging/demonstration.
    processor = SimpleSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    
    trace.set_tracer_provider(provider)
    _tracer_configured = True


def get_tracer(name: str):
    setup_tracing()
    return trace.get_tracer(name)
