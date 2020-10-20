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
import World.countries as countries
import Poland.poland_stats as pl

population = countries.load_countries_data()

with tracer.start_as_current_span(f"Poland weekly"):
    cases = ecdc.cases_by_country()
    testing = ecdc.testing_by_country_weekly()
    hospital_rates = ecdc.hospitel_admission_rates_weekly()

    data = ecdc.weekly(cases, "Poland", testing, hospital_rates)

# data = ecdc.weekly_all_countries(cases, testing, hospital_rates)


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

import pandas as pd
import plotly.graph_objects as go
import numpy as np


df_pl = pl.covid_19_timeline()

summary = df_pl.aggregate({pl.DEATHS_DAILY:['sum', 'max'], 
              pl.CONFIRMED_DAILY:['sum', 'max'],
              }) 

summary['confirmed ratio'] = summary[pl.CONFIRMED_DAILY]['sum']*100/population['Poland']
summary['country'] = 'Poland'
summary['active'] = df_pl[pl.ACTIVE][-1]
summary['active ratio'] = summary.active*100/population['Poland']
layout = dict(title = 'Covid19 ratio',
              geo = dict(projection = {'type':'mercator'}),
              height=800,
              margin={"r":0,"t":30,"l":0,"b":0}
             )

data = dict(
        
        type = 'choropleth',
        colorscale = 'Viridis',
        locations = summary['country'],
        locationmode = "country names",
        z = summary['confirmed ratio'],
        text = summary['country'],
        colorbar = {'title' : 'Ratio'},
      )



choromap = go.Figure(data = [data],layout = layout)

choromap.update_geos(
    visible=False, scope="europe",
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="Blue"
)
choromap.show()