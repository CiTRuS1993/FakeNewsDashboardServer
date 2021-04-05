import jsonpickle
from jsonpickle import json

from PersistenceLayer.AnalysisORM import AnalysedTweets, AnalyzedClaims, AnalysedTopics
from PersistenceLayer.ExternalAPIsORM import TweetORM, SnopesORM, TrendsORM


class AnalysisORMFacade:
    def __init__(self):
        from ..database import session
        self.session = session

    #   ----------------------- Tweets -----------------------

    def add_analyzed_tweet(self, id, prediction, emotion, sentiment):
        analyzed_tweet = AnalysedTweets(id=id, prediction=prediction, emotion=emotion, sentiment=sentiment)
        analyzed_tweet.add_to_db()
        tweet = self.session.query(TweetORM).filter_by(id=id).first()
        analyzed_tweet.tweet = tweet
        analyzed_tweet.update_db()

    def get_all_analyzed_tweets(self):
        tweets = jsonpickle.dumps(self.session.query(AnalysedTweets).all())
        jtweets = json.loads(tweets)
        tweets_dict = {}
        for tweet in jtweets:
            tweets_dict[tweet['id']] = tweet
        return tweets_dict

    def get_analyzed_tweet(self, id):
        tweet = jsonpickle.dumps(self.session.query(AnalysedTweets).filter_by(id=id).first())
        jtweet = json.loads(tweet)
        return jtweet

    #   ----------------------- Claims -----------------------

    def add_analyzed_claim(self, id, prediction, emotion, sentiment):
        analyzed_claim = AnalyzedClaims.AnalysedClaims(id=id, prediction=prediction, emotion=emotion,
                                                       sentiment=sentiment)
        analyzed_claim.add_to_db()
        claim = self.session.query(SnopesORM).filter_by(id=id).first()
        analyzed_claim.claim = claim
        analyzed_claim.update_db()

    def get_all_analyzed_claims(self): # TODO- BUG (on comment at analysisManager)
        claims = jsonpickle.dumps(self.session.query(AnalyzedClaims).all())
        jclaims = json.loads(claims)
        return jclaims

    def get_analyzed_claim(self, id):
        claim = jsonpickle.dumps(self.session.query(AnalyzedClaims).filter_by(id=id).first())
        jclaim = json.loads(claim)
        return jclaim

#   ----------------------- Topics -----------------------

    def add_analyzed_topic(self, key_words, prediction, emotion, sentiment, tweets_ids, trend_id):
        tweets = self.session.query(TweetORM.id.in_(tweets_ids)).all()
        trend = self.session.query(TrendsORM).filter_by(id=trend_id).first()
        topic = AnalysedTopics(key_words=key_words, prediction=prediction, emotion=emotion, sentiment=sentiment)
        topic.trend = trend
        topic.topic_tweets = tweets
        topic.add_to_db()
        return topic.id

    def get_all_analyzed_topics(self):
        topics = jsonpickle.dumps(self.session.query(AnalysedTopics).all())
        jtopics = json.loads(topics)
        return jtopics

    def get_analyzed_topic(self, key_words):
        topic = jsonpickle.dumps(self.session.query(AnalysedTopics).filter_by(key_words=key_words).first())
        jtopic = json.loads(topic)
        return jtopic


    # def __setitem__(self, key, value):
    #     self.add_user(**value)
    #
    # def __getitem__(self, username):
    #     return self.get_user(username)
    #
    # def __delitem__(self, username):
    #     self.delete_user()
    #
    # def __iter__(self):
    #     for user in self.session.query(UserOrm):
    #         yield json.loads(jsonpickle.dumps(user))