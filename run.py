# Configure opentelemetry. This has to be done before we import anything we want to trace
from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

RequestsInstrumentor().instrument()
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="COVID-19-notebook",
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchExportSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)
tracer = trace.get_tracer(__name__)

import World.ecdc as ecdc
import plotly.graph_objects as go

with tracer.start_as_current_span(f"Poland weekly"):
    cases = ecdc.cases_by_country()
    testing = ecdc.testing_by_country_weekly()
    hospital_rates = ecdc.hospitel_admission_rates_weekly()

    data = ecdc.weekly(cases, "Poland", testing, hospital_rates)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=[i["dateRep"] for i in data],
        y=[i["hospital_rate"] for i in data],
        mode="lines+markers",
        name="hospital rate",
    )
)

fig.add_trace(
    go.Scatter(
        x=[i["dateRep"] for i in data], y=[i["deaths"] for i in data], name="deaths"
    )
)

fig.add_trace(
    go.Bar(x=[i["dateRep"] for i in data], y=[i["cases"] for i in data], name="cases")
)
fig.show()
