#! /usr/bin/python
import twitter as tw
from config import settings
from Poland.tweets_mz import parse_tweets
from datetime import date


if __name__ == "__main__":
    t = tw.Twitter(
        auth=tw.OAuth(
            token=settings.TWITTER_ACCESS_TOKEN,
            token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_KEY_SECRET,
        )
    )

    df = parse_tweets(t)

    today_str = date.today().strftime("%Y.%m.%d")
    file_name = f"./Poland/MZ_Tweets/{today_str}-MZ_GOV_PL.csv"
    df.to_csv(file_name, index = False, header=True)

