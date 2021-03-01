import threading

from BuisnessLayer.AnalysisManager.ClassifierAdapter import ClassifierAdapter

# trend -> topics
# snopes claims
# on each one -> sentiment [-3,3], emotional, fake
from BuisnessLayer.AnalysisManager.DataObjects import Claim, Tweet, Trend
from PersistenceLayer.AnalysisORM.AnalysisORMFacade import AnalysisORMFacade


class AnalysisManager:

    def __init__(self):
        self.dashboard_statistics = {}
        self.trends_statistics = {}
        self.snopes_statistics = {}
        self.adapter = ClassifierAdapter()
        self.orm = AnalysisORMFacade()
        # TODO- retrieve previous analysis's from DB


    def getGoogleTrendsStatistics(self):
        return self.trends_statistics

    def getSnopesStatistics(self):
        return self.snopes_statistics

    # TODO
    def classifyTweets(self, file):
        # read file
        # self.adapter.analyze(data, callback)
        # save to DB
        pass

    def retrieveFakeNewsData(self):
        return self.dashboard_statistics

    # TODO
    def configClassifier(self, classifier, configuration):
        pass

    def add_new_trends_statistics(self, processed):
        # prev: processed is type of dict<trends> = (dict<claims> = (dict<tweets> = prediction, emotional, sentiment))
        for trend in processed.keys():  # processed is type of dict<trend name> = list <Claim>
            prediction = 0
            emotional = 0
            sentiment = 0
            ids = []
            for claim in processed[trend]:
                for tweet in claim.tweets:
                    ids.append(tweet.id)
                    sentiment = (sentiment + tweet.sentiment)
                    prediction = (prediction + tweet.is_fake)
                    emotional = (emotional + tweet.emotion)
                    # self.trends_statistics[trend][tweet] = processed[trend][tweet]
            avg_prediction = prediction / len(ids)
            avg_emotional = emotional / len(ids)
            avg_sentiment = sentiment / len(ids)
            if trend not in self.trends_statistics.keys():
                self.trends_statistics[trend] = Trend(processed[trend])
            self.orm.add_analyzed_topic(trend, avg_prediction, avg_emotional, avg_sentiment, ids,
                                        self.trends_statistics[trend]['id'])
            self.trends_statistics[trend]['id'] = self.trends_statistics[trend]['id'] + 1
            if 'sentiment' in self.trends_statistics[trend].keys():
                amount = self.trends_statistics[trend]['amount']
                avg_sentiment = ((avg_sentiment * len(ids)) + self.trends_statistics[trend]['sentiment']) / amount
                avg_emotional = ((avg_emotional * len(ids)) + self.trends_statistics[trend]['emotional']) / amount
                avg_prediction = ((avg_prediction * len(ids)) + self.trends_statistics[trend]['prediction']) / amount
            self.trends_statistics[trend] = {'sentiment': avg_sentiment, 'prediction': avg_prediction,
                                           'emotional': avg_emotional, 'amount': len(ids)}

    def classifyTrends(self, trends_tweets):
        def callback(processed):
            # save the new claims to DB
            for topic in processed.keys():
                claim = processed[topic]
                prediction = 0
                emotion = 0
                sentiment = 0
                for tweet in claim.tweets:
                    sentiment = (sentiment + tweet.sentiment)
                    prediction = (prediction + tweet.is_fake)
                    emotion = (emotion + tweet.emotion)
                    self.orm.add_analyzed_tweet(tweet.is_fake, tweet.emotion, tweet.sentiment)
                self.orm.add_analyzed_topic(prediction/len(claim.tweets), emotion/len(claim.tweets),
                                            sentiment/len(claim.tweets))
            # update statistics to show the new analyzed data
            # TODO
            self.add_new_trends_statistics(processed)
            self.dashboard_statistics = processed  # TODO: maybe =+ instead of =


        # fail = False
        # trends = {}
        # for trend in trends_tweets:
        #     trends[trend] = self.get_claims_from_trend(trends_tweets[trend])
        #     # if returns wrong output -> fail = True
        # analyze_thread = threading.Thread(target=self.adapter.analyze, args=(trends, callback))
        # analyze_thread.start()
        # return not fail

        trends = {}
        for trend in trends_tweets:
            claims= self.get_claims_from_trend(trends_tweets[trend]['tweets'])    # <trend_name> : list <Claim>
            trends[trend] = Trend(trends_tweets[trend]['id'], claims)
        analyze_thread = threading.Thread(target=self.adapter.analyze_trends, args=(trends, callback))
        analyze_thread.start()
        return True

    def classifySnopes(self, claims_tweets):
        def callback(processed):
            # update statistics to show the new analyzed data
            self.snopes_statistics += processed
            self.dashboard_statistics += processed  # TODO- maybe = instead of =+
            # save the new claims to DB
            sentiment = 0
            prediction = 0
            emotion = 0
            for claim in processed.keys():
                for tweet in claim.tweets:
                    self.orm.add_analyzed_tweet(tweet.is_fake, tweet.emotion, tweet.sentiment)
                    emotion = emotion + tweet.emotion
                    prediction = prediction + tweet.is_fake
                    sentiment = sentiment + tweet.sentiment
            self.orm.add_analyzed_claim(prediction, emotion, sentiment)

        # apply analyze concurrently on each new Snopes claim
        analyze_thread = threading.Thread(target=self.adapter.analyze_snopes, args=(claims_tweets, callback))
        analyze_thread.start()
        # for claim in claims_tweets.keys():
        #     analyze_thread = threading.Thread(target=self.adapter.analyze, args=(claims_tweets[claim], callback))
        #     analyze_thread.start()

    # send the tweets of some trend to the claims classifier and return its answer (claims)
    # initialize the data structures : Claim, Tweet
    # returns list <Claim>
    def get_claims_from_trend(self, trends_tweets):
        claims_dict = self.adapter.get_claims_from_trend(trends_tweets)
        claims = list()
        for key in claims_dict.keys():
            tweets = list()
            for tweet in claims_dict[key]:
                tweets.append(Tweet(tweet))  # tweet = id, author, content
            claim = Claim(key, tweets)
            claims.append(claim)
        return claims