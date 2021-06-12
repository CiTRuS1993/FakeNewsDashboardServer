import random
import threading
import time
import tweepy
from attr import dataclass
from tweepy import OAuthHandler

from PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade import ExternalAPIsORMFacade


@dataclass
class Token:
    id: int
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_secret: str

@dataclass
class Tweet:
    id: int
    author_name: str
    content: str
    location: str
    date: str
    trend_id: int
    retweet_count:int
    favorite_count:int


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
        self.orm = ExternalAPIsORMFacade()
        self.all_tweets = self.orm.get_all_tweets_dict()
        self.unprocessed_tweets = self.orm.get_unprocessed_tweets()
    def connect(self):
        to_select = self.tokens.keys()
        token = self.tokens[self.token_ids.pop(0)]

        auth = OAuthHandler(token.consumer_key,token.consumer_secret)
        auth.set_access_token(token.access_token, token.access_secret)
        auth = tweepy.OAuthHandler(token.consumer_key,token.consumer_secret)
        auth.set_access_token(token.access_token, token.access_secret)
        self.api = tweepy.API(auth)
        self.token_ids.append(token.id)


    def is_connected(self):
        return not self.api == None

    def search_tweets_by_keywords(self,trend_id, keywords, token=None, on_finished=lambda tweets: (tweets)):
        tweets = {}
        i = 1
        j=1
        for keyword in keywords:
            try:
                i = 0
                for tweet in tweepy.Cursor(self.api.search, q=keyword, lang='en').items(100):
                    i=i+1
                    if trend_id not in tweets.keys():
                        tweets[trend_id] = []
                    _tweet = Tweet(tweet.id, tweet.author.name, tweet.text,
                                   tweet.user.location, tweet.created_at, trend_id,tweet.favorite_count,tweet.retweet_count)
                    tweets[trend_id].append(_tweet)
                    if tweet.text not in self.all_tweets.values():
                        self.orm.add_tweet(tweet.id, tweet.author.name, tweet.text, 
                                           tweet.user.location, tweet.created_at,tweet.favorite_count,tweet.retweet_count,trend_id= trend_id)
                        try:
                            orm_tweet = self.orm.get_tweet(tweet.id)
                            tweet= Tweet(orm_tweet.id, orm_tweet.author_name, orm_tweet.content, orm_tweet.location,
                                  orm_tweet.date, trend_id,tweet.favorite_count,tweet.retweet_count)
                            # tweet= orm_tweet
                        except:
                            tweet= Tweet(tweet.id, tweet.author.name, tweet.text,
                                   tweet.user.location, tweet.created_at, trend_id,tweet.favorite_count,tweet.retweet_count)
                        self.all_tweets[tweet.id] = tweet
                    if i >= 900:
                        time.sleep(900)
            except:
                self.connect()
                j+=1
                if j>4:
                    j=0
                    break
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
                        if key not in self.unprocessed_tweets.keys():
                            self.unprocessed_tweets[key] = {'keyword':trends[trend]['keywords'],'tweets':new_tweets[key]}
                        else:
                            self.unprocessed_tweets[key]['tweets'] +=new_tweets[key]
                    if not self.search:
                        return
                time.sleep(900)

        search_thread = threading.Thread(target=search_trends)
        self.search = True
        search_thread.setDaemon(True)

        search_thread.start()

    def edit_tokens(self, tokens):
        for token in tokens:
            if token not in self.tokens.keys():
                self.tokens.append(token)    # bug, self.tokens is dict and not list!
        return True

    def get_unprocessed_tweets(self):
        tweets = self.unprocessed_tweets
        self.unprocessed_tweets = {}
        return tweets
