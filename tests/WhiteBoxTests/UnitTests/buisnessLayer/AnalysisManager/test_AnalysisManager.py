import time
from unittest import TestCase, mock

from BuisnessLayer.AnalysisManager.AnalysisManager import AnalysisManager
from tests.WhiteBoxTests.UnitTests.buisnessLayer.AnalysisManager.TestsObjects import Name, Trend, Claim, AnalysedTweet


class TestAnalysisManager(TestCase):

    def setUp(self) -> None:
        self.analysis_manager = AnalysisManager()
        self.trends_names = ['Donald Trump', 'Covid19', 'Elections']
        self.trends = {'Donald Trump': Trend(1, 'Donald Trump'), 'Covid19': Trend(2, 'Covid19'),
                       'Elections': Trend(3, 'Elections')}
        self.tweet1 =  {'id': '1', 'author':'aa', 'content': 'tweet1'}
        self.tweet2 =  {'id': '2', 'author':'aa', 'content': 'tweet2'}
        self.tweet3 =  {'id': '3', 'author':'aa', 'content': 'tweet3'}
        # self.tweet1_obj = Status('1', Name('aa'), 'tweet1')
        # self.tweet2_obj = Status('2', Name('aa'), 'tweet2')
        # self.tweet3_obj = Status('3', Name('aa'), 'tweet3')
        self.trends_tweets = {
            '1': {'id': 1, 'keyword': 'Donald Trump', 'tweets': (self.tweet1, self.tweet2, self.tweet3)},
            '2': {'id': 2, 'keyword': 'Covid19', 'tweets': (self.tweet1, self.tweet2, self.tweet3)},
            '3': {'id': 3, 'keyword': 'Elections', 'tweets': (self.tweet1, self.tweet2, self.tweet3)}}
        self.claims = {'claim1': {'1': self.tweet1, '3': self.tweet3},
                       'claim2': {'1': self.tweet1, '2': self.tweet2}}
        self.analysed_tweet1 = AnalysedTweet('1', Name('aa'), 'tweet1', 'Happy', 2, 'true')
        self.analysed_tweet2 = AnalysedTweet('2', Name('aa'), 'tweet2', 'Sad', -1, 'fake')
        self.analysed_tweet3 = AnalysedTweet('3', Name('aa'), 'tweet3', 'Sad', -3, 'true')
        self.trends_claims = {'1': [Claim('claim1', [self.analysed_tweet1, self.analysed_tweet2],1), Claim('claim2', [self.analysed_tweet2, self.analysed_tweet3],2)],
                              '2': [Claim('claim3', [self.analysed_tweet1, self.analysed_tweet2],3), Claim('claim4', [self.analysed_tweet1, self.analysed_tweet3],4)],
                              '3': [Claim('some claim', [self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3],5)]}
        self.snopes = {'claim1': [self.tweet1, self.tweet2, self.tweet3],
                       'claim2': [self.tweet1, self.tweet2, self.tweet3],
                       'claim3': [self.tweet1, self.tweet2, self.tweet3]}

    @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_classify_trends(self, mock):
        self.analysis_manager.adapter = mock
        # mock.analyze_trends.return_value =
        self.assertTrue(self.analysis_manager.classifyTrends(self.trends_tweets))

    @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_classify_snopes(self, mock):
        self.analysis_manager.adapter = mock
        self.analysis_manager.classifySnopes(self.snopes)

    @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_get_claims_from_trend(self, mock):
        self.analysis_manager.adapter = mock
        mock.get_claims_from_trend.return_value = self.claims
        for trend in self.trends_tweets.keys():
            claims = self.analysis_manager.get_claims_from_trend(self.trends_tweets[trend]['tweets'])
            self.assertTrue(len(claims) > 0)


    @mock.patch("PersistenceLayer.AnalysisORM.AnalysisORMFacade")
    def test_add_new_trends_statistics(self, mock):
        self.analysis_manager.orm = mock
        self.assertTrue(self.analysis_manager.add_new_trends_statistics(self.trends_claims))

    # @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    # def test_init_trend_statistics(self, mock_claims):
    #     self.fail()

        # def calc_topics_statistics_and_save(self, processed, topics_statistics, trend):
        #     words_cloud = dict()
        #     for topic in processed[trend]:
        #         prediction = {'true': 0, 'fake': 0}
        #         emotions = list()
        #         sentiment = 0
        #         ids = []
        #         for tweet in topic.tweets:
        #             for word in tweet.content.split():
        #                 if word in words_cloud:
        #                     words_cloud[word] = words_cloud[word] + 1
        #                 else:
        #                     words_cloud[word] = 1
        #             ids.append(tweet.id)
        #             sentiment = sentiment + tweet.sentiment
        #             prediction[tweet.is_fake] = prediction[tweet.is_fake] + 1
        #             emotions.append(tweet.emotion)
        #             if tweet.id not in self.orm_tweets:
        #                 self.orm.add_analyzed_tweet(tweet.id, tweet.is_fake, tweet.emotion,
        #                                             tweet.sentiment)
        #                 self.orm_tweets[tweet.id] = self.orm.get_analyzed_tweet(tweet.id)
        #         # update emotions statistics
        #         emotion = self.update_emotions(emotions)
        #         avg_prediction = self.calc_avg_prediction(prediction)
        #         topics_statistics.append((emotions, sentiment, prediction))
        #         self.orm.add_analyzed_topic(topic.name, avg_prediction, emotion, sentiment / len(emotions), ids, trend)
        #     words_cloud_statistics = list()
        #     for word in words_cloud.keys():
        #         words_cloud_statistics.append(WordCloud(word, words_cloud[word]))
        #     return words_cloud_statistics
        #

    @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_calc_topics_statistics_and_save(self, mock_claims):
        self.fail()

        # def get_trend_name(self, trend_id):
        #     flag = True
        #     trend_name = ''
        #     for analysed_trend_id in self.trends_statistics:
        #         if analysed_trend_id == trend_id:
        #             flag = False
        #             trend_name = self.trends_statistics[analysed_trend_id].keywords
        #     if flag:
        #         for keywords in self.trends:
        #             if trend_id == self.trends[keywords].id:
        #                 trend_name = keywords
        #                 flag = False
        #     if flag:
        #         print("problem in get_trend_name()")
        #     return trend_name

    def test_get_trend_name(self):
        self.analysisManager.trends_statistics = {'1': Trend(1, 'Donald Trump'), '2': Trend(2, 'Covid19'),
                                                  '3': Trend(3, 'Elections')}
        self.analysisManager.trends = self.trends
        assert self.analysisManager.get_trend_name('1') == 'Donald Trump'
        assert self.analysisManager.get_trend_name('2') == 'Covid19'
        assert self.analysisManager.get_trend_name('3') == 'Elections'

        #
        # def get_emotion_tweets(self, emotion):
        #     trends_tweets = list()
        #     snopes_tweets = list()
        #     for trend in self.trends_statistics:
        #         for topic in self.trends_statistics[trend].claims:
        #             trends_tweets = self.search_for_emotion_on_tweets(emotion, topic.tweets)
        #     for claim in self.snopes_statistics:
        #         snopes_tweets = self.search_for_emotion_on_tweets(emotion, claim.tweets)
        #     return trends_tweets + snopes_tweets
        #     # return {'tweets': [{'id': "1361577298282094592", 'emotion': "happy", 'real': "fake", 'sentiment': 3},
        #     #                    {'id': "1361577298282094592", 'emotion': "happy", 'real': "true", 'sentiment': 3}]}

    def test_get_tweets_by_emotion(self):
        self.analysisManager.classifyTrends(self.trends_tweets)
        time.sleep(10)
        emotion = self.analysisManager.getGoogleTrendsStatistics()['Donald Trump']['statistics']['emotion'][0]
        # print(emotion)
        # print(self.analysisManager.get_emotion_tweets(emotion))
        self.assertTrue(len(self.analysisManager.get_emotion_tweets(emotion)) > 0)

    # def update_emotions(self, emotions):
    #     # calculate the most repetitive emotion
    #     emotions_counter = {"Anger": 0, "Disgust": 0, "Sad": 0, "Happy": 0, "Surprise": 0, "Fear": 0}
    #     for emotion in emotions:
    #         emotions_counter[emotion] = emotions_counter[emotion] + 1
    #     max_emotion_counter = max([emotions_counter[emotion] for emotion in emotions_counter])
    #     max_emotion = [emotion for emotion in emotions_counter if emotions_counter[emotion] == max_emotion_counter]
    #     # update the emotions statistics
    #     for emotion_dict in self.emotions['emotions']:
    #         emotion_dict['amount'] = emotion_dict['amount'] + emotions_counter[emotion_dict['label']]
    #     return max_emotion
    #
    def test_update_emotions(self):
        self.fail()

        # def update_todays_sentiment(self, date):
        #     todays_trends_sentiment = {'sentiment': self.todays_sentiment['trends'], 'date': str(date)}
        #     todays_topics_sentiment = {'sentiment': self.todays_sentiment['topics'], 'date': str(date)}
        #     todays_claims_sentiment = {'sentiment': self.todays_sentiment['claims'], 'date': str(date)}
        #     self.sentiment.claims.append(todays_claims_sentiment)
        #     self.sentiment.topics.append(todays_topics_sentiment)
        #     self.sentiment.trends.append(todays_trends_sentiment)
        #

    def test_update_todays_sentiment(self):
        self.fail()

        # def addTrend(self, trend):
        #     keywords = ""
        #     for k in trend.keywords:
        #         keywords = keywords + k + ' '
        #     # print(self.trends)
        #     if keywords in self.trends:
        #         self.trends[keywords].statistics.statistics.copy_statistics(trend.statistics.statistics)
        #     else:
        #         self.trends[keywords] = trend

    def test_addTrend(self):
        self.fail()

        #
        # def get_topic(self, topic_id):
        #     for trend_name in self.trends_statistics:
        #         for topic in self.trends_statistics[trend_name]:
        #             if topic.id == topic_id:
        #                 return {'tweets': topic.tweets, 'emotions': topic.get_all_emotions}
        #     # error case (stub)
        #     print("Error on AnalysisManager.get_topic()")
        #     return {'tweets': [{'id': "1361577298282094592", 'emotion': "happy", 'real': "fake", 'sentiment': 3},
        #                        {'id': "1361577298282094592", 'emotion': "happy", 'real': "true", 'sentiment': -2}],
        #             'emotions': [{'y': 32, 'label': "Anger"},
        #                          {'y': 22, 'label': "Disgust"},
        #                          {'y': 15, 'label': "Sad"},
        #                          {'y': 19, 'label': "Happy"},
        #                          {'y': 5, 'label': "Surprise"},
        #                          {'y': 16, 'label': "Fear"}]}

    def test_get_topic(self):
        self.fail()

        #
        # def search_for_emotion_on_tweets(self, emotion, tweets) -> list:
        #     emotion_tweets = list()
        #     for tweet in tweets:
        #         if tweet.emotion == emotion:
        #             emotion_tweets.append(asdict(tweet))
        #     return emotion_tweets

    def test_search_for_emotion_on_tweets(self):
        self.fail()

        #
        # def getTemperature(self):
        #     is_fake = self.temperature['is_fake'] / self.temperature['amount']
        #     if is_fake < 0.5:
        #         is_fake = 0
        #     else:
        #         is_fake = 1
        #     temperature = Temperature(self.temperature['authenticity'],
        #                               round(self.temperature['sentiment'] / self.temperature['amount']),
        #                               is_fake)
        #     return temperature

    def test_get_temperature(self):
        self.fail()

        # def calc_avg_prediction(self, prediction):
        #     # if prediction['true'] > prediction['fake']:
        #     #     return 'true'
        #     # return 'fake'
        #     return prediction['true'] / len(prediction)

    def test_calc_avg_prediction(self):
        self.fail()



    # def test_config_classifier(self):
    #     self.fail()

    # def test_classify_tweets(self):
    #     self.fail()
