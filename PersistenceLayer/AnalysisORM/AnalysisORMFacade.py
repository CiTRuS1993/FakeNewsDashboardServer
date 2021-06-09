from datetime import datetime

import jsonpickle
from jsonpickle import json

from PersistenceLayer.AnalysisORM import AnalysedTweets, AnalyzedClaims, AnalysedTopics
from PersistenceLayer.ExternalAPIsORM import TweetORM, SnopesORM, TrendsORM
from PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade import ExternalAPIsORMFacade


class AnalysisORMFacade:
    def __init__(self):
        self.unsaved_tweets = {}
        from ..database import session
        self.session = session
        self.externalAPIs = ExternalAPIsORMFacade()

    #   ----------------------- Tweets -----------------------

    def add_analyzed_tweet(self, id, prediction, emotion, sentiment):
        try:
            analyzed_tweet = AnalysedTweets(id=id, prediction=prediction, emotion=emotion, sentiment=sentiment)
            try:
                tweet = self.session.query(TweetORM).filter_by(id=id).first()
                analyzed_tweet.tweet = tweet
                analyzed_tweet.add_to_db()
                return True
            except Exception as e:
                TweetORM.update_db()
                print("Try to commit analysed tweet to DB while there is no tweet with the given id")
            # print(f"tweet: {tweet.id}")
            # print(f"analyzed_tweet: {analyzed_tweet.id}")
            # analyzed_tweet.add_to_db()
            # self.session.flush()
        except:
            print(f"DB error! (Analysis.add_analyzed_tweet)")
            self.session.commit()
        return False

    def get_all_analyzed_tweets(self):
        tweets = jsonpickle.dumps(self.session.query(AnalysedTweets).all())
        jtweets = json.loads(tweets)
        tweets_dict = {}
        for tweet in jtweets:
            tweet_dict = {'prediction': tweet['prediction'], 'emotion': tweet['emotion'],
                           'sentiment': tweet['sentiment']}
            try:
                tweet_dict['tweet']= tweet['tweet']
            except:
                pass
            tweets_dict[tweet['id']] = tweet_dict
        return tweets_dict

    def get_analyzed_tweet(self, t_id):
        tweet = jsonpickle.dumps(self.session.query(AnalysedTweets).filter_by(id=t_id).first())
        jtweet = json.loads(tweet) # TODO- change format of jtweet
        return jtweet

    #   ----------------------- Claims -----------------------

    def add_analyzed_claim(self, c_id, prediction, emotion, sentiment):
        analyzed_claim = AnalyzedClaims.AnalysedClaims(id=c_id, prediction=prediction, emotion=emotion,
                                                       sentiment=sentiment)
        # analyzed_claim.add_to_db()
        claim = self.session.query(SnopesORM).filter_by(id=c_id).first()
        analyzed_claim.claim = claim
        analyzed_claim.update_db()
        # self.session.flush()
        # analyzed_claim.flush_db()


    def get_all_analyzed_claims(self): # TODO- BUG (on comment at analysisManager), try to uncomment after saving some analysed claims
        claims = jsonpickle.dumps(self.session.query(AnalyzedClaims).all())
        jclaims = json.loads(claims)
        return jclaims

    def get_analyzed_claim(self, id):
        claim = jsonpickle.dumps(self.session.query(AnalyzedClaims).filter_by(id=id).first())
        jclaim = json.loads(claim)
        return jclaim

#   ----------------------- Topics -----------------------
    def update_topic(self,id,key_words,prediction, emotion, sentiment):
        topic = self.session.query(AnalysedTopics).filter_by(id=id).first()
        topic.prediction  = prediction
        topic.emotion  = emotion
        topic.sentiment  = sentiment
        topic.update_db()

    def add_analyzed_topic(self, key_words, prediction, emotion, sentiment, tweets_ids, trend_id):
        if self.get_analyzed_topic(key_words) is not None:
            return False
        tweets = []
        # tweets = self.session.query(TweetORM.id.in_(tweets_ids)).all()
        for t_id in tweets_ids:
            try:
                tweet = self.session.query(TweetORM).filter_by(id=t_id).first()
                tweets.append(tweet)
            except:
                self.unsaved_tweets[trend_id]= {'claim keywords': key_words, 'tweet id': t_id}
                print("there is an unsaved tweet")
            # tweets.append(self.externalAPIs.get_tweet(t_id))
        # trend = self.session.query(TrendsORM).filter_by(id=trend_id)
        topic = AnalysedTopics(key_words=key_words, prediction=prediction, emotion=emotion, sentiment=sentiment)
        topic.add_to_db()
        try:
            trend = self.session.query(TrendsORM).filter_by(id=trend_id).all()
            topic.trend = trend
        except:
            print(f"problem on saving the trend-topic connection")
        try:
            topic.topic_tweets = tweets
            topic.update_db()
        except:
            print(f"there was no tweets to save on the ORM, tweets list= {tweets}")
        print(f"unsaved tweets: {self.unsaved_tweets}")
        return topic.id

    def get_all_analyzed_topics(self):
        topics = jsonpickle.dumps(self.session.query(AnalysedTopics).all())
        jtopics = json.loads(topics)
        topics_list = []
        for jtopic in jtopics:
            topic = {'keywords': jtopic['key_words'], 'prediction': jtopic['prediction'],
                    'emotion': jtopic['emotion'], 'sentiment': round(float(jtopic['sentiment']))}
            try:
                topic['tweets']= jtopic['topic_tweets']
                topic['trend']= jtopic['trend']
            except:
                pass
            topics_list.append(topic)
        return topics_list
        # return jtopics

    def get_analyzed_topic(self, key_words):
        try:
            topic = jsonpickle.dumps(self.session.query(AnalysedTopics).filter_by(key_words=key_words).first())
            jtopic = json.loads(topic) # TODO- change format of jtopic
            return jtopic
        except:
            print(f"problem at get_analyzed_topic(keywords={key_words})")
            return None

    def get_all_trends(self):
        # analysed_topics = self.get_all_analyzed_topics()
        # trends=[]
        # for at in analysed_topics:
        #     trends.append(at['trend'])
        # print(f"all analyzed trends on orm = {trends}")
        # return trends
        today_day = datetime.today().day
        if today_day - 12 > 0:
            date = datetime(datetime.today().year, datetime.today().month, today_day).date()
        elif datetime.today().month != 1:
            date = datetime(datetime.today().year, datetime.today().month-1, 30-today_day).date()
        else:
            date = datetime(datetime.today().year-1, 12, 31-today_day).date()
        return self.externalAPIs.get_trends_names_from_date(date)

    def get_trends_data(self,date):
        return self.externalAPIs.get_trends_data_from_date(date)
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