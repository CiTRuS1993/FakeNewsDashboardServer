from PersistenceLayer.AnalysisORM import AnalysedTweets, AnalyzedClaims, AnalysedTopics
from PersistenceLayer.ExternalAPIsORM import TweetORM, SnopesORM, TrendsORM


class AnalysisORMFacade:
    def __init__(self):
        from ..database import session
        self.session = session

    def add_analyzed_tweet(self, id, prediction, emotion, sentiment):
        analyzed_tweet = AnalysedTweets(id=id, prediction=prediction, emotion=emotion, sentiment=sentiment)
        analyzed_tweet.add_to_db()
        tweet = self.session.query(TweetORM).filter_by(id=id).first()
        analyzed_tweet.tweet = tweet
        analyzed_tweet.update_db()

    def add_analyzed_claim(self, id, prediction, emotion, sentiment):
        analyzed_claim = AnalyzedClaims.AnalysedClaims(id=id, prediction=prediction, emotion=emotion,
                                                       sentiment=sentiment)
        analyzed_claim.add_to_db()
        claim = self.session.query(SnopesORM).filter_by(id=id).first()
        analyzed_claim.claim = claim
        analyzed_claim.update_db()

    def add_analyzed_topic(self, key_words, prediction, emotion, sentiment, tweets_ids, trend_id):
        tweets = self.session.query(TweetORM.id.in_(tweets_ids)).all()
        trend = self.session.query(TrendsORM).filter_by(id=trend_id).first()
        topic = AnalysedTopics(key_words=key_words, prediction=prediction, emotion=emotion, sentiment=sentiment)
        topic.trend = trend
        topic.topic_tweets = tweets
        topic.add_to_db()
        return topic.id
