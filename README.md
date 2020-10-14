# COVID-19 data service

This data service collects data on confirmed cases, deaths, tests, hospitalization rates from multiple sources. Includes methods of data analysis to produce meaningful trend graphs and meaningful comparisons between countries based on their population.

There are plenty of web pages giving all of those data already. The aim of this code is to give full flexibility in the analysis using jupyter lab/notebook for the engineers or data scientists.

It also has opentelemetry monitoring setup to capture service telemetry data to better observe and debug issues with data ingestion from multiple sources and then data processing.

## Setup project

Create virtual environment

`python3 -m venv venv`

Activate venv and install dependencies

`. ./venv/bin/activate`

`pip install -r requirements.txt`

Run jupyter lab

`jupyter lab`

### Install and run telemetry backend

`sudo docker run -p 16686:16686 -p 6831:6831/udp jaegertracing/all-in-one`

## Contributing

You can contribute in the following ways:

* write documentation
* implement features
* fix bugs
* add tests
* give suggestions, share ideas etc...

Please format commit message using the conventional-changelog.

## Code style

Please use black as code formatter,

`pip install black`

`black .`
