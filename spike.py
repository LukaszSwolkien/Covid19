import time
import requests
import json

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.exporter import jaeger
from collections import Counter
from datetime import datetime


trace.set_tracer_provider(TracerProvider())
jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="covid19 data importer",
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchExportSpanProcessor(jaeger_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)


def covid19_case_distribution() -> list:
    URL = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
    PARAMS = {'countriesAndTerritories': 'Poland'}

    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    return data['records']


def covid19_monthly(data: list, country: str) -> dict:
    selector = lambda x: x['countriesAndTerritories']==country
    selected_data = list(filter(selector, data))
    sorted_selected_data = sorted(selected_data, key = lambda x: (int(x['month']), int(x['day'])))

    agg_data = dict()
    z_stats = {'cases': 0, 'deaths': 0}
    for v in sorted_selected_data:
        ym = v['year'] + '.' + v['month']
        cases = v['cases']
        deaths = v['deaths']
        curr = agg_data.get(ym, z_stats)
        summary = Counter(curr) + Counter({'cases': cases, 'deaths': deaths})
        agg_data[ym] = summary

    return agg_data


def covid19_daily(data: list, country: str, start_date: datetime, end_date: datetime) -> dict:
    selector = lambda x: (
        x['countriesAndTerritories']==country and 
    )
    selected_data = list(filter(selector, data))
    sorted_selected_data = sorted(selected_data, key = lambda x: (int(x['month']), int(x['day'])))

    agg_data = dict()
    z_stats = {'cases': 0, 'deaths': 0}
    for v in sorted_selected_data:
        ym = v['year'] + '.' + v['month']
        cases = v['cases']
        deaths = v['deaths']
        curr = agg_data.get(ym, z_stats)
        summary = Counter(curr) + Counter({'cases': cases, 'deaths': deaths})
        agg_data[ym] = summary

    return agg_data

with tracer.start_as_current_span('Case distribution'):
    data = covid19_case_distribution()
    print(f'recived data. Total elements {len(data)}')

    with tracer.start_as_current_span('Poland monthly'):
        agg_data = covid19_case_distribution_monthly(data, 'Poland')
        print(json.dumps(agg_data))




