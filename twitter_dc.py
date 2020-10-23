#! /usr/bin/python
QUERY_STRING = "#koronawiruspolska"
FREQUENCY_SEC = 600

from opentelemetry import metrics
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricsExporter
from opentelemetry.sdk.metrics.export.controller import PushController

metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__, True)
exporter = ConsoleMetricsExporter()
controller = PushController(meter, exporter, 5)

staging_labels = {"environment": "staging"}

requests_counter = meter.create_metric(
    name="requests",
    description=f"{QUERY_STRING} tweets",
    unit="1",
    value_type=int,
    metric_type=Counter,
    # label_keys=("environment",),
)


import twitter as tw
from config import settings
from Poland.tweets_mz import total_cases_and_deaths
from datetime import date, datetime, timedelta
import time
from dateutil.parser import parse
from dateutil.tz import tzutc


if __name__ == "__main__":
    t = tw.Twitter(
        auth=tw.OAuth(
            token=settings.TWITTER_ACCESS_TOKEN,
            token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_KEY_SECRET,
        )
    )

    df = total_cases_and_deaths(t)

    today_str = date.today().strftime("%Y.%m.%d")
    file_name = f"./Poland/MZ_Tweets/{today_str}-MZ_GOV_PL.csv"
    df.to_csv(file_name, index = False, header=True)

    while True:
        covid_tweets = t.search.tweets(q=QUERY_STRING)
        s = covid_tweets.get('statuses', [])

        now =  datetime.now(tzutc())
        x_ago = now - timedelta(seconds=FREQUENCY_SEC)
        selected = [item for item in s if parse(item['created_at'])>x_ago]
        no_selected = len(selected)
        requests_counter.add(no_selected, staging_labels)
        for tweet in selected:
            print(f"[{tweet['user']['name']}]{tweet['text']}")
        time.sleep(FREQUENCY_SEC)

#     created_at = parse(first['created_at'])
#     tzinfo = created_at.tzinfo


