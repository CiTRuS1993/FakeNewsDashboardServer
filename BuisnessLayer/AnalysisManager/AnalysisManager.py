import datetime
import threading
from dataclasses import asdict

import schedule

from BuisnessLayer.AnalysisManager.ClassifierAdapter import ClassifierAdapter

# trend -> topics
# snopes claims
# on each one -> sentiment [-3,3], emotional, fake
from BuisnessLayer.AnalysisManager.DataObjects import *
from PersistenceLayer.AnalysisORM.AnalysisORMFacade import AnalysisORMFacade


class AnalysisManager:

    def __init__(self):
        self.trends = {}
        self.todays_sentiment = {'trends': 0, 'topics': 0, 'claims': 0} # TODO- update after new tweets
        self.sentiment = Sentiment([{'sentiment': 1, 'date': "1.3.2021"}, {'sentiment': 2, 'date': "2.3.2021"}],
                                   [{'sentiment': -1, 'date': "1.3.2021"}, {'sentiment': -2, 'date': "2.3.2021"}],
                                   [{'sentiment': 0, 'date': "1.3.2021"}, {'sentiment': 3, 'date': "2.3.2021"}])
        # self.sentiment = Sentiment([{'y': 1, 'label': "1.3.2021"}, {'y': 2, 'label': "2.3.2021"}],
        #                            [{'y': -1, 'label': "1.3.2021"}, {'y': -2, 'label': "2.3.2021"}],
        #                            [{'y': 0, 'label': "1.3.2021"}, {'y': 3, 'label': "2.3.2021"}])
    #         {
    #     'topics': [
    #         {'y': 1, 'label': "1.1.2021"},
    #         {'y': 1, 'label': "2.1.2021"},
    #         {'y': -1, 'label': "3.1.2021"},
    #         {'y': 1, 'label': "4.1.2021"},
    #         {'y': 2, 'label': "5.1.2021"},
    #         {'y': 1, 'label': "6.1.2021"},
    #         {'y': 3, 'label': "7.1.2021"},
    #         {'y': -1, 'label': "8.1.2021"},
    #         {'y': 1, 'label': "9.1.2021"},
    #         {'y': 1, 'label': "10.1.2021"},
    #         {'y': -3, 'label': "11.1.2021"},
    #         {'y': 1, 'label': "12.1.2021"}
    #     ], 'trends': [
    #         {'y': 3, 'label': "1.1.2021"},
    #         {'y': 1, 'label': "2.1.2021"},
    #         {'y': 0, 'label': "3.1.2021"},
    #         {'y': 0, 'label': "4.1.2021"},
    #         {'y': 0, 'label': "5.1.2021"},
    #         {'y': 0, 'label': "6.1.2021"},
    #         {'y': 1, 'label': "7.1.2021"},
    #         {'y': -1, ' label': "8.1.2021"},
    #         {'y': 1, 'label': "9.1.2021"},
    #         {'y': 1, 'label': "10.1.2021"},
    #         {'y': 1, 'label': "11.1.2021"},
    #         {'y': -2, 'label': "12.1.2021"}
    #     ],
    #     'claims': [
    #         {'y': 1, 'label': "1.1.2021"},
    #         {'y': 1, 'label': "2.1.2021"},
    #         {'y': 3, 'label': "3.1.2021"},
    #         {'y': 2, 'label': "4.1.2021"},
    #         {'y': -1, ' label': "5.1.2021"},
    #         {'y': 1, 'label': "6.1.2021"},
    #         {'y': 1, 'label': "7.1.2021"},
    #         {'y': 0, 'label': "8.1.2021"},
    #         {'y': -3, ' label': "9.1.2021"},
    #         {'y': 1, 'label': "10.1.2021"},
    #         {'y': -2, ' label': "11.1.2021"},
    #         {'y': 1, 'label': "12.1.2021"}
    #     ]
    # }
        self.emotions = self.init_emotions_dict()
        self.temperature = {'sentiment': 0, 'is_fake': 0, 'authenticity': 15, 'amount': 1}
        self.dashboard_statistics = {}
        self.trends_statistics = {}
        self.snopes_statistics = {}
        self.adapter = ClassifierAdapter()
        self.orm = AnalysisORMFacade()
        # TODO- retrieve previous analysis's from DB
        schedule.every().day.at("23:57").do(lambda :(self.update_todays_sentiment(datetime.date.today())))

    def init_emotions_dict(self):
        return {'emotions': [
            {'amount': 0, 'label': "Anger"},
            {'amount': 0, 'label': "Disgust"},
            {'amount': 0, 'label': "Sad"},
            {'amount': 0, 'label': "Happy"},
            {'amount': 0, 'label': "Surprise"},
            {'amount': 0, 'label': "Fear"}
        ]}

    # should return dict of <trend name> : TrendStatistics asdict --> asdict(trend.statistics)
    def getGoogleTrendsStatistics(self):
        current_statistics = dict()
        for trend in self.trends_statistics:
            current_statistics[trend] = asdict(self.trends_statistics[trend].statistics)
        return current_statistics

    def getSnopesStatistics(self):
        return self.snopes_statistics # TODO- like getGoogleTrendsStatistics()

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
        for trend in processed.keys():  # processed is type of dict<trend name> = list <Claim>
            topics_statistics = list()
            trend_id = self.get_trend_id(trend)
            self.calc_topics_statistics_and_save(processed, topics_statistics, trend)
            # ------------------- TODO- sync -----------------------
            if trend not in self.trends_statistics.keys():
                first = True
                for (emotions, sentiment, prediction) in topics_statistics:
                    if first and len(emotions)>0:
                        first = False
                        trend_statistics = self.init_trend_statistics(emotions, prediction, sentiment)
                        self.trends_statistics[trend] = AnalysedTrend(trend_id, trend, processed[trend], trend_statistics) # TODO- maybe already is an AnalysedTrend (in proccessed)
                    else:
                        self.trends_statistics[trend].statistics.statistics.add_statistics(emotions, sentiment, prediction)
            # --------------------- until here ---------------------
    def init_trend_statistics(self, emotions, prediction, sentiment):
        emotion = self.update_emotions(emotions)
        avg_prediction = self.calc_avg_prediction(prediction)
        statistics = Statistics(emotion, sentiment / len(emotions), avg_prediction, 50, len(emotions))
        trend_statistics = TrendStatistic(["this", "is", "a", "words", "cloud"], statistics)
        return trend_statistics

    def calc_topics_statistics_and_save(self, processed, topics_statistics, trend):
        for topic in processed[trend]:
            prediction = {'true': 0, 'fake': 0}
            emotions = list()
            sentiment = 0
            ids = []
            for tweet in topic.tweets:
                ids.append(tweet.id)
                sentiment = sentiment + tweet.sentiment
                prediction[tweet.is_fake] = prediction[tweet.is_fake] + 1
                emotions.append(tweet.emotion)
                # self.orm.add_analyzed_tweet(tweet.id, tweet.is_fake, tweet.emotion, tweet.sentiment) TODO UNCOMMENT
            # update emotions statistics
            emotion = self.update_emotions(emotions)
            avg_prediction = self.calc_avg_prediction(prediction)
            topics_statistics.append((emotions, sentiment, prediction))
            # self.orm.add_analyzed_topic(topic.name, avg_prediction, emotion, sentiment/len(emotions), ids, trend_id)  TODO UNCOMMENT

    def get_trend_id(self, trend):
        flag = True
        for analysed_trend in self.trends_statistics:
            if analysed_trend == trend:
                flag = False
                trend_id = self.trends_statistics[analysed_trend].id
        if flag:
            for trend_name in self.trends:
                if trend == trend_name:
                    trend_id = self.trends[trend_name].id
        return trend_id

    def classifyTrends(self, trends_tweets):
        def callback(processed):
            # update statistics to show the new analyzed data and save it to DB
            self.add_new_trends_statistics(processed)
            # self.dashboard_statistics = processed  # TODO: maybe =+ instead of =
            return True

        trends = {}
        for trend_name in trends_tweets:
            claims= self.get_claims_from_trend(trends_tweets[trend_name]['tweets'])    # <trend_name> : list <Claim>
            trend = Trend(trends_tweets[trend_name]['id'], trend_name, claims)
            trends[trend_name] = trend
            self.addTrend(trend)
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
            prediction = {'true': 0, 'fake': 0}
            emotions = list()
            for claim in processed.keys():
                for tweet in claim.tweets:
                    self.orm.add_analyzed_tweet(tweet.id, tweet.is_fake, tweet.emotion, tweet.sentiment)
                    emotions.append(tweet.emotion)
                    prediction[tweet.is_fake] = prediction[tweet.is_fake] + 1
                    sentiment = sentiment + tweet.sentiment
            # update emotions statistics
            emotion = self.update_emotions(emotions)
            print(f"max emotion on this snopes is {emotion}")
            avg_prediction = self.calc_avg_prediction(prediction)
            self.orm.add_analyzed_claim(avg_prediction, emotion, sentiment/len(emotions))

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
            for tweet_id in claims_dict[key]:
                tweets.append(Tweet(tweet_id, claims_dict[key][tweet_id]['author'], claims_dict[key][tweet_id]['content']))  # tweet = id, author, content
            claim = Claim(key, tweets)
            claims.append(claim)
        return claims

    def getTemperature(self):
        temperature = Temperature(self.temperature['authenticity'], self.temperature['sentiment']/self.temperature['amount'],
                                  self.temperature['is_fake']/self.temperature['amount'])
        return temperature

    def get_emotions(self):
        # print(f"emotions: {self.emotions}")
        return self.emotions

    def update_emotions(self, emotions):
        # calculate the most repetitive emotion
        emotions_counter = {"Anger":0, "Disgust":0, "Sad":0, "Happy":0, "Surprise": 0, "Fear": 0}
        for emotion in emotions:
            emotions_counter[emotion] = emotions_counter[emotion]+1
        max_emotion_counter = max([emotions_counter[emotion] for emotion in emotions_counter])
        max_emotion = [emotion for emotion in emotions_counter if emotions_counter[emotion]==max_emotion_counter]
        # update the emotions statistics
        for emotion_dict in self.emotions['emotions']:
            emotion_dict['amount'] = emotion_dict['amount'] + emotions_counter[emotion_dict['label']]
        return max_emotion

    def calc_avg_prediction(self, prediction):
        # if prediction['true'] > prediction['fake']:
        #     return 'true'
        # return 'fake'
        return prediction['true'] / len(prediction)

    def get_sentiment(self):
        return self.sentiment

    def update_todays_sentiment(self, date):
        todays_trends_sentiment = {'sentiment': self.todays_sentiment['trends'], 'date': str(date)}
        todays_topics_sentiment = {'sentiment': self.todays_sentiment['topics'], 'date': str(date)}
        todays_claims_sentiment = {'sentiment': self.todays_sentiment['claims'], 'date': str(date)}
        self.sentiment.claims.append(todays_claims_sentiment)
        self.sentiment.topics.append(todays_topics_sentiment)
        self.sentiment.trends.append(todays_trends_sentiment)

    def addTrend(self, trend):
        if trend.keywords in self.trends:
            self.trends[trend.keywords].statistics.statistics.copy_statistics(trend.statistics.statistics)
        else:
            self.trends[trend.keywords] = trend