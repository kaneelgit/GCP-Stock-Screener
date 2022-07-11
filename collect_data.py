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

#get setimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

#get tickers
tickers = pd.read_csv('data/tickers.csv')

#get main dataframe
main_df = pd.read_csv('data/main_dataframe.csv').set_index('Ticker')

#get setimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
