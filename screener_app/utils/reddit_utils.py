"""
Author - Kaneel Senevirathne
Date - 07/05/2022
"""

import praw
from utils import credentials
import pandas as pd
import re
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import numpy as np
from datetime import datetime

class scrape_data:

    def __init__(self, client_id, secret, user_id):
        
        #initialize reddit credentials
        self.client_id = client_id
        self.secret = secret
        self.user_id = user_id
        
        #initialize sentimentanalyzer
        self.sid = SentimentIntensityAnalyzer()

        #initialze data collection methods
        self.mentioned = []
        tickers_df = pd.read_csv('data/tickers.csv')
        self.ticker_list = tickers_df['Ticker'].to_list()

        #initialize polarity dictionary
        self.polarity = {ticker: 0 for ticker in self.ticker_list}

        #instance
        self.reddit = praw.Reddit(
            client_id = self.client_id,
            client_secret = self.secret, 
            user_agent = self.user_id
            )

        subreddit = ["wallstreetbets", "investing", "stocks"]

        #collect data from the subreddits
        for subred in subreddit:
            self.scrape_subreddit_data(subred)
        
        #create dataframe
        self.create_df()
    
    def scrape_subreddit_data(self, subred):
        """
        Scrape data given a subreddit
        """
        
        for i, submission in enumerate(self.reddit.subreddit(subred).hot(limit = None)):

            sub = re.sub(r'[^\w\s]', '', submission.title)
            sub_split = sub.split()

            text = re.sub(r'[^\w\s]', '', submission.selftext)
            text_split = text.split()

            for ticker in self.ticker_list:
                if ticker in sub_split:
                    self.mentioned.append(ticker)
                    pol_sub = self.sid.polarity_scores(submission.title)['compound']
                    self.polarity[ticker] += pol_sub

                if ticker in text_split:
                    self.mentioned.append(ticker)
                    pol_text = self.sid.polarity_scores(submission.selftext)['compound']
                    self.polarity[ticker] += pol_text
    
    def create_df(self):
        """
        Creates a csv file and save data
        """
        #create dataframe to save
        td = datetime.today()
        td_str = f'{td.month}_{td.day}_{td.year}'
        col_count = f"count_{td_str}"
        col_sentiment = f"sentiment_{td_str}"
        df = pd.DataFrame(index = self.ticker_list, columns = [col_count, col_sentiment])

        for t in np.unique(self.mentioned):
            #count how many times the stock was mentioned
            count = self.mentioned.count(t)
            df[col_count].loc[str(t)] = count

            #divide the polarity by the count to average the polairty score
            self.polarity[t] /= count
            df[col_sentiment].loc[str(t)] = self.polarity[t]

        df = df.reset_index()
        df.to_csv(f"results/results_{td_str}.csv", index = False)
    
if __name__ == "__main__":
    data_scraper = scrape_data(credentials.client_id, credentials.secret, credentials.user_id)


