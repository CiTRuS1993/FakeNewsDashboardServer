import random
import threading
import time
import tweepy
from attr import dataclass
from tweepy import OAuthHandler

class TwitterManager:
    def __init__(self):
        self.unprocessed_tweets = {}
        self.tokens= {}
        self.search = False
        self.token= Token(consumer_key= 'tWsXjgFakSqxuoB1lfRaJMBX4',consumer_secret = 'CmyellBME94ZCmU2MxcSrd0qcj9BZMWRnIApnoOAQC8oXJqkeQ',
        access_token = '1353027459139174401-pe4YnxZsHfFav8ZbmZIXuyyNbhgAwd',access_secret = 'fAvqCeXtcCK6iYZFNVJkbLYBPPJaUjmfyBBtPfhSe956B')
        self.tokens[0]=self.token
        self.api = None

    def connect(self):
        to_select = self.tokens.keys()
        num = random.randint(0, len(to_select)-1)

        auth = OAuthHandler(self.tokens[num].consumer_key, self.tokens[num].consumer_secret)
        auth.set_access_token(self.tokens[num].access_token, self.tokens[num].access_secret)
        auth = tweepy.OAuthHandler(self.tokens[num].consumer_key,self.tokens[num].consumer_secret)
        auth.set_access_token(self.token.access_token, self.token.access_secret)
        self.api = tweepy.API(auth)

    def search_tweets_by_keywords(self,trend_id, keywords, token=None, on_finished=lambda tweets: print(tweets)):
        tweets = {}
        for keyword in keywords:
            for tweet in tweepy.Cursor(self.api.search, q=keyword, lang='en').items():
                if keyword not in tweets.keys():
                    tweets[trend_id] = []
                tweets[trend_id].append(tweet)
        on_finished(tweets)
        return tweets

    def stop(self):
        self.search = False

    def search_tweets_by_trends(self, trends):
        # trends={'id': {}}
        def search_trends():
            while self.search:
                for trend in trends.keys():
                    new_tweets = self.search_tweets_by_keywords(trend,trends[trend]['keywords'], self.tokens[0])
                    for key in new_tweets.keys():
                        self.unprocessed_tweets[key] = {'keyword':trends[trend]['keywords'],'tweets':new_tweets[key]}
                    if not self.search:
                        return

        search_thread = threading.Thread(target=search_trends)
        self.search = True
        search_thread.start()

    def edit_tokens(self, token):
        for token in token:
            if token not in self.tokens.keys():
                self.tokens.append(token)

    def get_unprocessed_tweets(self):
        tweets = self.unprocessed_tweets
        self.unprocessed_tweets = {}
        return tweets

@dataclass
class Token:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_secret: str