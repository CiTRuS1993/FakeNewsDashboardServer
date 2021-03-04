import datetime
import threading
from dataclasses import asdict
from threading import Lock
import schedule

from BuisnessLayer.AnalysisManager.ClassifierAdapter import ClassifierAdapter
from BuisnessLayer.AnalysisManager.DataObjects import *
from PersistenceLayer.AnalysisORM.AnalysisORMFacade import AnalysisORMFacade


class AnalysisManager:

    def __init__(self):
        self.trends = {}
        self.lock = Lock()
        self.todays_sentiment = {'trends': 0, 'topics': 0, 'claims': 0}
        self.sentiment = Sentiment([{'sentiment': 2, 'date': "27.2.2021"}, {'sentiment': 1, 'date': "28.2.2021"}, {'sentiment': 1, 'date': "1.3.2021"}, {'sentiment': 2, 'date': "2.3.2021"}, {'sentiment': 2, 'date': "3.3.2021"}],
                                   [{'sentiment': -1, 'date': "27.2.2021"}, {'sentiment': 0, 'date': "28.2.2021"}, {'sentiment': -1, 'date': "1.3.2021"}, {'sentiment': -2, 'date': "2.3.2021"}, {'sentiment': -2, 'date': "3.3.2021"}],
                                   [{'sentiment': -2, 'date': "27.2.2021"}, {'sentiment': 2, 'date': "28.2.2021"}, {'sentiment': 0, 'date': "1.3.2021"}, {'sentiment': 3, 'date': "2.3.2021"}, {'sentiment': 1, 'date': "3.3.2021"}])
        self.emotions = self.init_emotions_dict()
        # self.emotion_tweets = {"Anger":list(), "Disgust": list(), "Sad":list(), "Happy": list(), "Surprise": list(), "Fear": list()}
        self.temperature = {'sentiment': 0, 'is_fake': 0, 'authenticity': 15, 'amount': 1}
        # self.dashboard_statistics = {}
        self.trends_statistics = {}
        self.snopes_statistics = {}
        self.adapter = ClassifierAdapter()
        self.orm = AnalysisORMFacade()
        # TODO- retrieve previous analysis's from DB
        schedule.every().day.at("23:57").do(lambda: (self.update_todays_sentiment(datetime.date.today())))

    def init_emotions_dict(self):
        return {'emotions': [
            {'amount': 1, 'label': "Anger"},
            {'amount': 1, 'label': "Disgust"},
            {'amount': 1, 'label': "Sad"},
            {'amount': 1, 'label': "Happy"},
            {'amount': 1, 'label': "Surprise"},
            {'amount': 1, 'label': "Fear"}
        ]}

    # should return dict of <trend name> : TrendStatistics asdict --> asdict(trend.statistics)
    def getGoogleTrendsStatistics(self):
        current_statistics = dict()
        for trend in self.trends_statistics:
            current_statistics[self.get_trend_name(trend)] = asdict(self.trends_statistics[trend].statistics)
        return current_statistics

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
        for trend_id in processed.keys():  # processed is type of dict<trend name> = list <Claim>
            topics_statistics = list()
            trend_name = self.get_trend_name(trend_id)
            words_cloud = self.calc_topics_statistics_and_save(processed, topics_statistics, trend_id)
            # -------------------- sync -----------------------
            self.lock.acquire()
            if trend_id not in self.trends_statistics.keys():
                first = True
                for (emotions, sentiment, prediction) in topics_statistics:
                    if first and len(emotions) > 0:
                        first = False
                        trend_statistics = self.init_trend_statistics(emotions, prediction, sentiment, words_cloud)
                        self.trends_statistics[trend_id] = AnalysedTrend(trend_id, trend_name, processed[trend_id],
                                                                      trend_statistics)
                    else:
                        try:
                            self.trends_statistics[trend_id].statistics.statistics.add_statistics(emotions, sentiment,
                                                                                               prediction)
                        except:
                            trend_statistics = self.init_trend_statistics(emotions, prediction, sentiment, words_cloud)
                            self.trends_statistics[trend_id] = AnalysedTrend(trend_id, trend_name, processed[trend_id],
                                                                          trend_statistics)
                self.lock.release()
            # --------------------- until here ---------------------
            return True

    def init_trend_statistics(self, emotions, prediction, sentiment, words_cloud):
        emotion = self.update_emotions(emotions)
        avg_prediction = self.calc_avg_prediction(prediction)
        if len(emotions) > 0:
            trend_sentiment = sentiment / len(emotions)
        else:
            trend_sentiment = sentiment
        statistics = Statistics(emotion, trend_sentiment, avg_prediction, 50, len(emotions))
        trend_statistics = TrendStatistic(words_cloud, statistics)
        return trend_statistics

    def calc_topics_statistics_and_save(self, processed, topics_statistics, trend):
        words_cloud = dict()
        for topic in processed[trend]:
            prediction = {'true': 0, 'fake': 0}
            emotions = list()
            sentiment = 0
            ids = []
            for tweet in topic.tweets:
                for word in tweet.content.split():
                    if word in words_cloud:
                        words_cloud[word] = words_cloud[word] + 1
                    else:
                        words_cloud[word] = 1
                ids.append(tweet.id)
                sentiment = sentiment + tweet.sentiment
                prediction[tweet.is_fake] = prediction[tweet.is_fake] + 1
                emotions.append(tweet.emotion)
                # self.orm.add_analyzed_tweet(tweet.id, tweet.is_fake, tweet.emotion, tweet.sentiment) TODO UNCOMMENT
            # update emotions statistics
            emotion = self.update_emotions(emotions)
            avg_prediction = self.calc_avg_prediction(prediction)
            topics_statistics.append((emotions, sentiment, prediction))
            # self.orm.add_analyzed_topic(topic.name, avg_prediction, emotion, sentiment/len(emotions), ids, trend)  TODO UNCOMMENT
        words_cloud_statistics = list()
        for word in words_cloud.keys():
            words_cloud_statistics.append(WordCloud(word, words_cloud[word]))
        return words_cloud_statistics

    def get_trend_name(self, trend_id):
        flag = True
        for analysed_trend_id in self.trends_statistics:
            if analysed_trend_id == trend_id:
                flag = False
                trend_name = self.trends_statistics[analysed_trend_id].keywords
        if flag:
            for keywords in self.trends:
                if trend_id == self.trends[keywords].id:
                    trend_name = keywords
                    flag = False
        if flag:
            print ("problem in get_trend_name()")
        return trend_name

    def classifyTrends(self, trends_tweets):
        trends = {}
        for trend_id in trends_tweets:
            claims = self.get_claims_from_trend(trends_tweets[trend_id]['tweets'])  # <trend_name> : list <Claim>
            trend = Trend(trend_id, trends_tweets[trend_id]['keyword'], claims)
            trends[trend_id] = trend
            self.addTrend(trend)
        analyze_thread = threading.Thread(target=self.adapter.analyze_trends,
                                          args=(trends, self.add_new_trends_statistics))
        analyze_thread.start()
        return True

    def classifySnopes(self, claims_tweets):
        def callback(processed):
            # calculate the claims statistics
            sentiment = 0
            prediction = {'true': 0, 'fake': 0}
            emotions = list()
            for claim in processed.keys():
                for tweet in processed[claim].tweets:
                    # self.orm.add_analyzed_tweet(tweet.id, tweet.is_fake, tweet.emotion, tweet.sentiment)  TODO - uncomment
                    emotions.append(tweet.emotion)
                    prediction[tweet.is_fake] = prediction[tweet.is_fake] + 1
                    sentiment = sentiment + tweet.sentiment
                # update emotions statistics
                emotion = self.update_emotions(emotions)
                avg_prediction = self.calc_avg_prediction(prediction)
                if len(emotions) > 0:
                    avg_sentiment = sentiment / len(emotions)
                else:
                    avg_sentiment = sentiment
                # save the new claims to DB
                # self.orm.add_analyzed_claim(claim.name, avg_prediction, emotion, avg_sentiment)   TODO - uncomment and name is instead of id
                # update statistics to display the new analyzed data
                # if claim in self.snopes_statistics:
                self.lock.acquire()
                try:
                    self.snopes_statistics[claim].add_statistics(emotions, sentiment, prediction)
                # else:
                except:
                    statistics = Statistics(emotion[0], avg_sentiment, avg_prediction, 15, len(emotions))
                    analysed_claim = AnalysedClaim(claim, processed[claim].tweets, statistics)
                    self.snopes_statistics[claim] = analysed_claim
                self.lock.release()
            return True

        # apply analyze concurrently on each new Snopes claim
        analyze_thread = threading.Thread(target=self.adapter.analyze_snopes, args=(claims_tweets, callback))
        analyze_thread.start()

    # send the tweets of some trend to the claims classifier and return its answer (claims)
    # initialize the data structures : Claim, Tweet
    # returns list <Claim>
    def get_claims_from_trend(self, trends_tweets):
        claims_dict = self.adapter.get_claims_from_trend(trends_tweets)
        claims = list()
        for key in claims_dict.keys():
            tweets = list()
            for tweet_id in claims_dict[key]:
                tweets.append(Tweet(tweet_id, claims_dict[key][tweet_id]['author'],
                                    claims_dict[key][tweet_id]['content']))  # tweet = id, author, content
            claim = Claim(key, tweets)
            claims.append(claim)
        return claims

    def getTemperature(self):
        temperature = Temperature(self.temperature['authenticity'],
                                  self.temperature['sentiment'] / self.temperature['amount'],
                                  self.temperature['is_fake'] / self.temperature['amount'])
        return temperature

    def get_emotions(self):
        # print(f"emotions: {self.emotions}")
        return self.emotions

    def update_emotions(self, emotions):
        # calculate the most repetitive emotion
        emotions_counter = {"Anger": 0, "Disgust": 0, "Sad": 0, "Happy": 0, "Surprise": 0, "Fear": 0}
        for emotion in emotions:
            emotions_counter[emotion] = emotions_counter[emotion] + 1
        max_emotion_counter = max([emotions_counter[emotion] for emotion in emotions_counter])
        max_emotion = [emotion for emotion in emotions_counter if emotions_counter[emotion] == max_emotion_counter]
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
        keywords = ""
        for k in trend.keywords:
            keywords = keywords + k + ' '
        # print(self.trends)
        if keywords in self.trends:
            self.trends[keywords].statistics.statistics.copy_statistics(trend.statistics.statistics)
        else:
            self.trends[keywords] = trend

    def get_topic(self, topic_id):
        for trend_name in self.trends_statistics:
            for topic in self.trends_statistics[trend_name]:
                if topic.id == topic_id:
                    return {'tweets': topic.tweets, 'emotions': topic.get_all_emotions}
        return {'tweets': [{'id': "1361577298282094592", 'emotion': "happy", 'real': "fake", 'sentiment': 3},
                           {'id': "1361577298282094592", 'emotion': "happy", 'real': "true", 'sentiment': -2}],
                'emotions': [{'y': 32, 'label': "Anger"},
                             {'y': 22, 'label': "Disgust"},
                             {'y': 15, 'label': "Sad"},
                             {'y': 19, 'label': "Happy"},
                             {'y': 5, 'label': "Surprise"},
                             {'y': 16, 'label': "Fear"}]}

    def get_emotion_tweets(self, emotion):
        trends_tweets = list()
        snopes_tweets = list()
        for trend in self.trends_statistics:
            for topic in self.trends_statistics[trend].claims:
                trends_tweets = self.search_for_emotion_on_tweets(emotion, topic.tweets)
        for claim in self.snopes_statistics:
            snopes_tweets = self.search_for_emotion_on_tweets(emotion, claim.tweets)
        return trends_tweets + snopes_tweets
        return {'tweets': [{'id': "1361577298282094592", 'emotion': "happy", 'real': "fake", 'sentiment': 3},
                           {'id': "1361577298282094592", 'emotion': "happy", 'real': "true", 'sentiment': 3}]}

    def search_for_emotion_on_tweets(self, emotion, tweets) -> list:
        emotion_tweets = list()
        for tweet in tweets:
            if tweet.emotion == emotion:
                emotion_tweets.append(asdict(tweet))
        return emotion_tweets
