#testing some stuff


import praw, credentials
import pandas as pd
import re
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter


sid = SentimentIntensityAnalyzer()

#get tickers
tickers = pd.read_csv('data/tickers.csv')

#instance
reddit = praw.Reddit(
    client_id = credentials.client_id,
    client_secret = credentials.secret, 
    user_agent = credentials.user_id
)

#mentioned stocks
mentioned  = []
ticker_list = tickers['Ticker'].to_list()[:10]
# print(ticker_list)


for i, submission in enumerate(reddit.subreddit("stocks").hot(limit = None)):

    # score = sid.polarity_scores(submission.title)['compound']
    # if float(score) > 0.2: 
    #     print(submission.title, score)
    sub = re.sub(r'[^\w\s]', '', submission.title)
    sub_split = sub.split()

    text = re.sub(r'[^\w\s]', '', submission.selftext)
    text_split = text.split()

    for ticker in ticker_list:
        if ticker in sub_split:
            mentioned.append(ticker)
        if ticker in text_split:
            mentioned.append(ticker)

for i, submission in enumerate(reddit.subreddit("investing").hot(limit = None)):

    # score = sid.polarity_scores(submission.title)['compound']
    # if float(score) > 0.2: 
    #     print(submission.title, score)
    sub = re.sub(r'[^\w\s]', '', submission.title)
    sub_split = sub.split()

    text = re.sub(r'[^\w\s]', '', submission.selftext)
    text_split = text.split()

    for ticker in ticker_list:
        if ticker in sub_split:
            mentioned.append(ticker)
        if ticker in text_split:
            mentioned.append(ticker)

for i, submission in enumerate(reddit.subreddit("wallstreetbets").hot(limit = None)):

    # score = sid.polarity_scores(submission.title)['compound']
    # if float(score) > 0.2: 
    #     print(submission.title, score)
    sub = re.sub(r'[^\w\s]', '', submission.title)
    sub_split = sub.split()

    text = re.sub(r'[^\w\s]', '', submission.selftext)
    text_split = text.split()

    for ticker in ticker_list:
        if ticker in sub_split:
            mentioned.append(ticker)
        if ticker in text_split:
            mentioned.append(ticker)


            
print(mentioned)

import matplotlib.pyplot as plt

plt.hist(mentioned)
plt.savefig('test.jpg')

