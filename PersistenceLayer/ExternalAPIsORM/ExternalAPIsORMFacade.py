from datetime import datetime

import jsonpickle
from jsonpickle import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from BuisnessLayer.AnalysisManager.DataObjects import AnalyzedTweet, AnalysedClaim, Statistics, Trend,Tweet
from PersistenceLayer.ExternalAPIsORM import AuthorORM, SearchORM, SnopesORM
from PersistenceLayer.ExternalAPIsORM.TrendsORM import TrendsORM
from PersistenceLayer.ExternalAPIsORM.TweetORM import TweetORM
from PersistenceLayer.BaseORM import dblock


class ExternalAPIsORMFacade:
    def __init__(self):
        # from ..database import session
        SQLALCHEMY_DATABASE_URL = "./test.db"

        engine = create_engine(
            "sqlite:///" + SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False},
            poolclass=StaticPool)

        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = Session()
        self.session = session

    def add_trend(self, content, date):
        trend = TrendsORM(content=content, date=date)
        trend.add_to_db()
        return trend.id

    def get_all_trends(self):
        trends = jsonpickle.dumps(self.session.query(TrendsORM).all())
        jtrends = json.loads(trends)
        trends_dict = {}
        for trend in jtrends:
            new_trend = {'date': trend['date'], 'id': trend['id']}
            if trend['content'] in trends_dict.keys():
                trends_dict[trend['content']].append(new_trend)
            else:
                trends_dict[trend['content']] = [new_trend]
        return trends_dict

    def get_trends_names_from_date(self, date):
        jtrends = self.get_all_trends()
        trends = {}
        for trend in jtrends.keys():
            for trend_instance in jtrends[trend]:
                if self.compare_dates(trend_instance['date'], date) >= 0:
                    trends[trend] = trend_instance
        return trends

    def get_trend(self, id):
        trend = jsonpickle.dumps(self.session.query(TrendsORM).filter_by(id=id).first())
        jtrend = json.loads(trend)
        trends_dict = {}

        new_trend = {'date': jtrend['date'], 'id': jtrend['id']}
        if jtrend['content'] in trends_dict.keys():
            trends_dict[jtrend['content']].append(new_trend)
        else:
            trends_dict[jtrend['content']] = [new_trend]

        return [new_trend]

    def add_author(self, username, statuses_count=0, followers_count=0, friends_count=0, listed_count=0):
        AuthorORM(username=username, statuses_count=statuses_count, followers_count=followers_count,
                  friends_count=friends_count, listed_count=listed_count).add_to_db()

    def add_tweet_to_author(self, tweet_id, author_username):
        tweet = self.session.query(TweetORM).filter_by(id=tweet_id).first()
        author = self.session.query(AuthorORM).filter_by(username=author_username).first()
        if author is not None:
            author.tweets.append(tweet)
            author.update_db()
        else:
            self.add_author(author_username)
            author = self.session.query(AuthorORM).filter_by(username=author_username).first()
            author.tweets.append(tweet)
            author.update_db()

    def add_tweet(self, id, author_username, content, location, date,favorite_count,retweet_count, trend_id=None, claim_id=None, is_test=False):
        if self.get_tweet(id) is not None:
            return False
        tweet = TweetORM(id=id, author_name=author_username, content=content, date=date, location=location,favorite_count=favorite_count,retweet_count=retweet_count)
        tweet.add_to_db(self.session)
        if trend_id is not None:
            trend = self.session.query(TrendsORM).filter_by(id=trend_id).first()
            if trend is not None:
                trend.tweets.append(tweet)
                dblock.acquire()
                self.session.commit()
                dblock.release()
                
        if claim_id is not None:
            claim = self.session.query(SnopesORM).filter_by(claim_id=claim_id).first()
            if claim is not None:
                claim.snope_tweets.append(tweet)
        self.add_tweet_to_author(id, author_username)
        # self.session.commit()
        try:
            if (not is_test) or (trend_id is not None) or (claim_id is not None):
                tweet.update_db()
            return True
        except:
            return False
    def get_unprocessed_tweets(self):
        unprocessed_trend = self.session.query(TrendsORM).filter_by(trend_topics=None)
        unprocessed_dict = {}
        for trend in unprocessed_trend:
            unprocessed_dict[trend.id] = {'keyword':trend.content,'tweets':[Tweet(tweet.id, tweet.author_name, tweet.content,
                                   tweet.location, tweet.date, trend.id,tweet.retweet_count,tweet.favorite_count) for tweet in trend.tweets]}
        return unprocessed_dict
    def get_all_tweets_dict(self):
        tweets = jsonpickle.dumps(self.session.query(TweetORM).all())
        jtweets = json.loads(tweets)
        tweets_dict = {}
        for tweet in jtweets:
            tweets_dict[tweet['id']] = tweet
        return tweets_dict

    def get_tweet(self, id):
        tweet = jsonpickle.dumps(self.session.query(TweetORM).filter_by(id=id).first())
        jtweet = json.loads(tweet)
        return jtweet

    def add_search(self, keywords):
        search = SearchORM(KeyWords=keywords)
        search.add_to_db()
        return search.search_id

    def add_snopes(self, content, Verdict, Date):
        snope = SnopesORM(content=content, Verdict=Verdict, Date=Date)
        snope.add_to_db()
        return snope.claim_id

    def compare_dates(self, date1, date2):
        if type(date1) is str:
            if len(date1) > 10:
                date1 = date1[:10]
            if '-' in date1:
                date1 = datetime(int(date1[:4]), int(date1[5:7]), int(date1[8:])).date()
            else:
                date1 = datetime(int("20" + date1[6:]), int(date1[3:5]), int(date1[:2])).date()
        if date1.year != date2.year:
            if date1.year > date2.year:
                return 1
            else:
                return -1
        elif date1.month != date2.month:
            if date1.month > date2.month:
                return 1
            else:
                return -1
        elif date1.day == date2.day:
            return 0
        elif date1.day > date2.day:
            return 1
        else:
            return -1

    def get_trends_data_from_date(self, date):

        trends = self.session.query(TrendsORM).all()
        tr = {}
        for t in trends:
            if self.compare_dates(t.date, date) >= 0:
                topics = []
                if len(t.topics)>0 and all(len(top.tweets)>0 for top in t.topics):
                    for topic in t.topics:
                        tweets = []
                        for tw in topic.tweets:
                            if tw.analyzed:
                                tweets.append(
                                   
                                    AnalyzedTweet(tw.id, tw.author_name, tw.content,tw.location,tw.date,t.id,tw.favorite_count,tw.retweet_count, tw.analyzed.emotion, tw.analyzed.sentiment,
                                                  tw.analyzed.prediction))
                        topics.append(AnalysedClaim(topic.key_words, tweets, topic.id,
                                                    Statistics(topic.emotion, topic.sentiment, topic.prediction, 
                                                               len(tweets))))

                    tr[t.content] = Trend(t.id, t.content, topics)
        return tr