import random
import threading
import time
import tweepy
from attr import dataclass
from tweepy import OAuthHandler



@dataclass
class Token:
    id: int
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_secret: str

#consumer_key = 'nMRLa7RAv9lT6j8akRWCy6UGD'
#consumer_secret = 'jHZYUnXNj6oSQTXqMicZ077NCOfMD7atDcjBLszAy6qfDlJBml'
#access_token = '1315318156509040641-CM8vvE8fApKSpq8NKgXES4HCYAJK3X'
#access_secret = 'rQSQvP8RYn36vP6uN49lEquujq9muVYwOGmcyv9pFkAxA'

class TwitterManager:
    def __init__(self):
        self.unprocessed_tweets = {}
        self.tokens = {}
        self.search = False
        self.token = Token(id=0, consumer_key= 'tWsXjgFakSqxuoB1lfRaJMBX4',consumer_secret = 'CmyellBME94ZCmU2MxcSrd0qcj9BZMWRnIApnoOAQC8oXJqkeQ',
                        access_token = '1353027459139174401-pe4YnxZsHfFav8ZbmZIXuyyNbhgAwd',access_secret = 'fAvqCeXtcCK6iYZFNVJkbLYBPPJaUjmfyBBtPfhSe956B')
        self.tokens[0]=self.token
        self.tokens[1]= Token(id=1, consumer_key= 'nMRLa7RAv9lT6j8akRWCy6UGD',consumer_secret = 'jHZYUnXNj6oSQTXqMicZ077NCOfMD7atDcjBLszAy6qfDlJBml',
                        access_token = '1315318156509040641-CM8vvE8fApKSpq8NKgXES4HCYAJK3X',access_secret = 'rQSQvP8RYn36vP6uN49lEquujq9muVYwOGmcyv9pFkAxA')
        self.token_ids = list(self.tokens.keys())
        self.api = None

    def connect(self):
        to_select = self.tokens.keys()
        token = self.tokens[self.token_ids.pop(0)]

        auth = OAuthHandler(token.consumer_key,token.consumer_secret)
        auth.set_access_token(token.access_token, token.access_secret)
        auth = tweepy.OAuthHandler(token.consumer_key,token.consumer_secret)
        auth.set_access_token(token.access_token, token.access_secret)
        self.api = tweepy.API(auth)
        self.token_ids.append(token.id)


    def search_tweets_by_keywords(self,trend_id, keywords, token=None, on_finished=lambda tweets: print(tweets)):
        tweets = {}
        i = 0
        for keyword in keywords:
            try:
                for tweet in tweepy.Cursor(self.api.search, q=keyword, lang='en').items(2):
                    if trend_id not in tweets.keys():
                        tweets[trend_id] = []
                    tweets[trend_id].append(tweet)
                    print(tweet.text,tweet.author,tweet.created_at)

                   # if i%100 == 0:
                       # time.sleep(360)
                   # i += 1
            except:
                self.connect()
                # self.search_tweets_by_keywords(trend_id, keywords)        TODO

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
