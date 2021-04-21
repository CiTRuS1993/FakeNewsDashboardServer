import jsonpickle
from jsonpickle import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from PersistenceLayer.ExternalAPIsORM import AuthorORM, SearchORM, SnopesORM
from PersistenceLayer.ExternalAPIsORM.TrendsORM import TrendsORM
from PersistenceLayer.ExternalAPIsORM.TweetORM import TweetORM


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

    def get_trend(self, id):
        trend = jsonpickle.dumps(self.session.query(TrendsORM).filter_by(id=id).first())
        jtrend = json.loads(trend)
        return jtrend

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

    def add_tweet(self, id, author_username, content, location, date, trend_id=None, claim_id=None):
        tweet = TweetORM(id=id, author_name=author_username, content=content, date=date, location=location)
        tweet.add_to_db()
        if trend_id is not None:
            trend = self.session.query(TrendsORM).filter_by(id=trend_id).first()
            if trend is not None:
                trend.tweets.append(tweet)
                trend.update_db()
        if claim_id is not None:
            claim = self.session.query(SnopesORM).filter_by(claim_id=claim_id).first()
            if claim is not None:
                claim.snope_tweets.append(tweet)
                claim.update_db()
        self.add_tweet_to_author(id, author_username)

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
