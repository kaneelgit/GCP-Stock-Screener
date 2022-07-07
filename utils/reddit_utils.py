"""
Author - Kaneel Senevirathne
Date - 07/05/2022
"""

from typing_extensions import Self
import praw
import pandas as pd

class reddit_data:

    def __init__(self, client_id, secret, user_id):

        self.client_id = client_id
        self.secret = secret
        self.user_id = user_id

        #instance
        self.reddit = praw.Reddit(
            lient_id = self.client_id,
            client_secret = self.secret, 
            user_agent = self.user_id
            )
        
    