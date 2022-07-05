#testing some stuff


import praw, credentials
import pandas as pd
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
ticker_list = tickers['Ticker'].to_list()
# print(ticker_list)
import time

tick = time.time()

for submission in reddit.subreddit("stocks").hot(limit = 10):

    # score = sid.polarity_scores(submission.title)['compound']
    # if float(score) > 0.2: 
    #     print(submission.title, score) 
    for comment in submission.comments:
        pass

tock = time.time()

print(tock - tick)  

