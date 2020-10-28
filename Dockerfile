FROM nikolaik/python-nodejs:python3.8-nodejs12

WORKDIR /covid19

COPY ["requirements.txt", "settings.yaml", ".secrets.yaml", "__init__.py", "config.py", "./"]

RUN python -m pip install -r requirements.txt
RUN jupyter labextension install jupyterlab-plotly

COPY ["common", "./common"]
COPY ["notebooks", "./notebooks"]
COPY ["Poland", "./Poland"]
COPY ["tests", "./tests"]
COPY ["World", "./World"]
CMD jupyter lab --ip=0.0.0.0 --allow-root
