import pandas as pd
import re
import twitter as tw

TWEET_STARTING_WITH = 'Liczba zakażonych koronawirusem'
TWEET_MIDDLE = '/'
TWEET_ENDING_WITH = '\(wszystkie pozytywne przypadki/w tym osoby zmarłe\)' 

def parse_tweets(t: tw.Twitter) -> pd.DataFrame:
    # Most of the code below is copy-pasted from https://github.com/anuszka/COVID-19-MZ_GOV_PL/blob/master/code/TwitterCaptureMZ_GOV_PL.py

    timeline = t.statuses.user_timeline(screen_name="MZ_GOV_PL")
    df=pd.DataFrame.from_dict(timeline)

    df_confirmed_deaths=df[df['text'].str.contains(TWEET_STARTING_WITH, na=False)]
    df_confirmed_deaths = df_confirmed_deaths.reindex(
        df_confirmed_deaths.columns.tolist() + ['confirmed','deaths'], axis=1) 
    # Find the numbers of confirmed cases and deaths in df_confirmed_deaths['text'].
    # Write these numbers in the 'confirmed' and 'deaths' columns.
    for index, row in df_confirmed_deaths.iterrows():
        tweet_text = row['text']
        result = re.search('%s(.*)%s(.*)%s' % (TWEET_STARTING_WITH, TWEET_MIDDLE, TWEET_ENDING_WITH), tweet_text)
        confirmed_str, deaths_str = result.group(1), result.group(2)
        confirmed_str=confirmed_str.replace(" ","")
        deaths_str=deaths_str.replace(" ","")
        confirmed_sanitized = re.search("([0-9]+)",confirmed_str).group(1)
        deaths_sanitized = re.search("([0-9]+)",deaths_str).group(1)
        confirmed = int(confirmed_sanitized)
        deaths = int(deaths_sanitized)
        df_confirmed_deaths.loc[index,'confirmed'] = confirmed
        df_confirmed_deaths.loc[index,'deaths'] = deaths

    df_confirmed_deaths = df_confirmed_deaths.astype({'confirmed': int, 'deaths': int})
    df_confirmed_deaths = df_confirmed_deaths.reset_index(drop=True)
    return df_confirmed_deaths[['created_at', 'confirmed', 'deaths']]
