# COVID-19 data service

This code collects data on confirmed cases, deaths, tests, hospitalization rates from multiple sources. Includes methods of data analysis to produce meaningful trend graphs and meaningful comparisons between countries based on their population.

There are many websites already providing all this data. The purpose of this code is to provide complete flexibility in jupyter lab / notebook analysis for anyone with Python skills who want to check data for themselves


## Setup project

Create virtual environment

`python3 -m venv venv`

Activate venv and install dependencies

`. ./venv/bin/activate`

`pip install -r requirements.txt`

Run jupyter lab

`jupyter lab`

### (Optional) install and run telemetry backend

This code has **opentelemetry** tracing embeded to better observe and debug issues. This service is simple but makes a few data sourcing calls and then calls several data processing methods so is a good place to check opentelemetry-python implementation.

Please note: This is **optional** step for someone who wants to play around with opentelemetry and observe the functions being tracked. 

* run Jaeger backend from docker

`sudo docker run -p 16686:16686 -p 6831:6831/udp jaegertracing/all-in-one`

* run Jaeger UI

`http://localhost:16686/`

* run `jupyther lab` then open `notebooks/ternds.ipynb` and go to above Jaeger UI to choose following service:

`COVID-19-notebook`

* browse details in `COVID-19-notebook: Poland daily` and `COVID-19-notebook: Countries weekly` to see all operations, durations of processing and tags

## Contributing

Read [how you can contribute](CONTRIBUTING.md)
