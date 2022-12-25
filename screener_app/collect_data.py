#collect data from reddit

#testing some stuff
import praw, credentials
import pandas as pd
import re
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

#date today
td = datetime.today()
td_str = f'{td.month}_{td.day}_{td.year}'

#get setimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

#get tickers
tickers = pd.read_csv('data/tickers.csv')

#get main dataframe
main_df = pd.read_csv('data/main_dataframe.csv').set_index('Ticker')

#create new columsn in main_df
#count
col_count = f'count_{td_str}'
col_nlp = f'nlp_{td_str}'

main_df[col_count] = np.nan
main_df[col_nlp] = np.nan

#get setimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

#instance
reddit = praw.Reddit(
    client_id = credentials.client_id,
    client_secret = credentials.secret, 
    user_agent = credentials.user_id
)

#mentioned stocks
mentioned  = []
ticker_list = tickers['Ticker'].to_list()

#get polarity of stocks
polarity = {ticker: 0 for ticker in ticker_list}


for i, submission in enumerate(reddit.subreddit("stocks").hot(limit = None)):

    # score = sid.polarity_scores(submission.title)['compound']

    sub = re.sub(r'[^\w\s]', '', submission.title)
    sub_split = sub.split()

    text = re.sub(r'[^\w\s]', '', submission.selftext)
    text_split = text.split()

    for ticker in ticker_list:
        if ticker in sub_split:
            mentioned.append(ticker)
            pol_sub = sid.polarity_scores(submission.title)['compound']
            polarity[ticker] += pol_sub
            
        if ticker in text_split:
            mentioned.append(ticker)
            pol_text = sid.polarity_scores(submission.selftext)['compound']
            polarity[ticker] += pol_text
            

for i, submission in enumerate(reddit.subreddit("investing").hot(limit = None)):

    # score = sid.polarity_scores(submission.title)['compound']

    sub = re.sub(r'[^\w\s]', '', submission.title)
    sub_split = sub.split()

    text = re.sub(r'[^\w\s]', '', submission.selftext)
    text_split = text.split()

    for ticker in ticker_list:
        if ticker in sub_split:
            mentioned.append(ticker)
            pol_sub = sid.polarity_scores(submission.title)['compound']
            polarity[ticker] += pol_sub
            
        if ticker in text_split:
            mentioned.append(ticker)
            pol_text = sid.polarity_scores(submission.selftext)['compound']
            polarity[ticker] += pol_text


for i, submission in enumerate(reddit.subreddit("wallstreetbets").hot(limit = None)):

    # score = sid.polarity_scores(submission.title)['compound']

    sub = re.sub(r'[^\w\s]', '', submission.title)
    sub_split = sub.split()

    text = re.sub(r'[^\w\s]', '', submission.selftext)
    text_split = text.split()

    for ticker in ticker_list:
        if ticker in sub_split:
            mentioned.append(ticker)
            pol_sub = sid.polarity_scores(submission.title)['compound']
            polarity[ticker] += pol_sub
            
        if ticker in text_split:
            mentioned.append(ticker)
            pol_text = sid.polarity_scores(submission.selftext)['compound']
            polarity[ticker] += pol_text

#append all the data 
for t in np.unique(mentioned):

    #collect the number of mentions 
    count = mentioned.count(t)
    main_df[col_count].loc[str(t)] = count

    polarity[t] /= count
    main_df[col_nlp].loc[str(t)] = polarity[t]

#save the csv
main_df.to_csv('data/main_dataframe.csv')