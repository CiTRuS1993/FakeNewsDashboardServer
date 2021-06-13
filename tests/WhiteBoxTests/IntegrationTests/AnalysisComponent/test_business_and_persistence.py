import time
from datetime import datetime
import unittest
from unittest import TestCase, mock
import pandas as pd

from BuisnessLayer.AnalysisManager.AnalysisManager import AnalysisManager, Temperature
from tests.WhiteBoxTests.UnitTests.buisnessLayer.AnalysisManager.TestsObjects import Trend, AnalysedTweet, Name, Claim, \
    name, AnalysedTrend, AnalysedClaim


class TestBusinessLayer(TestCase):

    def setUp(self) -> None:
        self.analysis_manager = AnalysisManager()
        self.trends_names = ['Donald Trump', 'Covid19', 'Elections']
        self.trends = {'Donald Trump': Trend(1, 'Donald Trump'), 'Covid19': Trend(2, 'Covid19'),
                       'Elections': Trend(3, 'Elections')}
        self.tweet1 = {'id': '1', 'author':'aa', 'content': 'tweet1'}
        self.tweet2 = {'id': '2', 'author':'aa', 'content': 'tweet2'}
        self.tweet3 = {'id': '3', 'author':'aa', 'content': 'tweet3'}
        self.trends_tweets = {
            '1': {'id': 1, 'keyword': 'Donald Trump', 'tweets': (self.tweet1, self.tweet2, self.tweet3)},
            '2': {'id': 2, 'keyword': 'Covid19', 'tweets': (self.tweet1, self.tweet2, self.tweet3)},
            '3': {'id': 3, 'keyword': 'Elections', 'tweets': (self.tweet1, self.tweet2, self.tweet3)}}
        self.claims = {'claim1': {'1': self.tweet1, '3': self.tweet3},
                       'claim2': {'1': self.tweet1, '2': self.tweet2}}
        self.analysed_tweet1 = AnalysedTweet('1', name('aa'), 'tweet1', 'Happy', 2, 1)
        self.analysed_tweet2 = AnalysedTweet('2', name('aa'), 'tweet2', 'Sad', -1, 0)
        self.analysed_tweet3 = AnalysedTweet('3', name('aa'), 'tweet3', 'Sad', -3, 1)
        self.analysed_tweets = [self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3]
        self.trends_claims = {'1': [Claim('claim1', [self.analysed_tweet1, self.analysed_tweet2],1),
                                    Claim('claim2', [self.analysed_tweet2, self.analysed_tweet3], 2)],
                              '2': [Claim('claim3', [self.analysed_tweet1, self.analysed_tweet2], 3),
                                    Claim('claim4', [self.analysed_tweet1, self.analysed_tweet3], 4)],
                              '3': [Claim('some claim', [self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3], 5)]}
        self.trends_topics = [
                              Claim('claim1', [self.analysed_tweet1, self.analysed_tweet2], 1),
                              Claim('claim2', [self.analysed_tweet2, self.analysed_tweet3], 2),
                              Claim('claim3', [self.analysed_tweet1, self.analysed_tweet2], 3),
                              Claim('claim4', [self.analysed_tweet1, self.analysed_tweet3], 4),
                              Claim('some claim',[self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3], 5)
                                ]
        self.snopes = {'claim1': [self.tweet1, self.tweet2, self.tweet3],
                       'claim2': [self.tweet1, self.tweet2, self.tweet3],
                       'claim3': [self.tweet1, self.tweet2, self.tweet3]}

    @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_classify_trends(self, classifier_mock):
        self.analysis_manager.adapter = classifier_mock
        classifier_mock._get_claim_from_trend.return_value= self.trends_topics
        self.assertTrue(self.analysis_manager.classifyTrends(self.trends_tweets)) # should add the trend to DB first

    def test_classify_snopes(self):
        length = len(self.analysis_manager.getSnopesStatistics())
        self.analysis_manager.classifySnopes(self.snopes)
        self.assertTrue(length < len(self.analysis_manager.getSnopesStatistics()))

    @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_get_claims_from_trend(self, adapter_mock):
        self.analysis_manager.adapter = adapter_mock
        adapter_mock._get_claim_from_trend.return_value= self.trends_topics
        for trend in self.trends_tweets.keys():
            claims = self.analysis_manager.get_claims_from_trend(self.trends_tweets[trend]['tweets'])
            self.assertTrue(len(claims) > 0)


    def test_add_new_trends_statistics(self):
        results = pd.DataFrame({'pred':[0, 0, 1, 1, 0, 0, 0, 1, 0, 1], 'author_guid':[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
        res= {'author_guid':12, False: {'pred':results['pred'].apply(lambda x:"True" if x else "Fake")},
              True: {'pred':results['pred'].apply(lambda x:"True" if x else "Fake")}}
        self.assertTrue(self.analysis_manager.add_new_trends_statistics(self.trends_claims, self.trends, res)>0)
        # no trends dict
        self.assertTrue(self.analysis_manager.add_new_trends_statistics(self.trends_claims, {}, res) > 0)


    def test_calc_topics_statistics_and_save(self):
        results = pd.DataFrame({'pred': [0, 0, 1, 1, 0, 0, 0, 1, 0, 1], 'author_guid': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
        res = {'author_guid': 12, False: {'pred': results['pred'].apply(lambda x: "True" if x else "Fake")},
               True: {'pred': results['pred'].apply(lambda x: "True" if x else "Fake")}}
        trends = {'Donald Trump': [Claim('claim1', [self.analysed_tweet1, self.analysed_tweet2], 1),
                                   Claim('claim2', [self.analysed_tweet2, self.analysed_tweet3], 2),
                                   Claim('claim3', [self.analysed_tweet1, self.analysed_tweet2], 3),
                                   Claim('claim4', [self.analysed_tweet1, self.analysed_tweet3], 4),
                                   Claim('some claim', [self.analysed_tweet1, self.analysed_tweet2,
                                                        self.analysed_tweet3], 5)]}
        words_cloud_statistics, topics_statistics= self.analysis_manager.calc_topics_statistics_and_save(
                                                    trends, [], "Donald Trump", res)
        self.assertTrue(len(words_cloud_statistics)>0)  # the DB has no such tweets
        self.assertTrue(len(topics_statistics)>0)

    def test_get_trend_name(self):
        self.analysis_manager.trends_statistics = {'1': Trend(1, 'Donald Trump'), '2': Trend(2, 'Covid19'),
                                                  '3': Trend(3, 'Elections')}
        self.analysis_manager.trends = self.trends
        assert self.analysis_manager.get_trend_name('1', self.trends) == 'Donald Trump'
        assert self.analysis_manager.get_trend_name('2', self.trends) == 'Covid19'
        assert self.analysis_manager.get_trend_name('3', self.trends) == 'Elections'

    @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_get_tweets_by_emotion(self, adapter_mock):
        self.analysis_manager.adapter = adapter_mock
        adapter_mock._get_claim_from_trend.return_value= self.trends_topics
        trends = {'Donald Trump': AnalysedTrend(1, 'Donald Trump',
                        [AnalysedClaim('claim1', [self.analysed_tweet1, self.analysed_tweet2], 1),
                        AnalysedClaim('claim2', [self.analysed_tweet2, self.analysed_tweet3], 2),
                        AnalysedClaim('claim3', [self.analysed_tweet1, self.analysed_tweet2], 3),
                        AnalysedClaim('claim4', [self.analysed_tweet1, self.analysed_tweet3], 4),
                        AnalysedClaim('some claim',[self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3], 5)])}
        self.analysis_manager.trends_statistics = trends
        res = self.analysis_manager.getGoogleTrendsStatistics()
        emotion = res['Donald Trump']['emotion']
        emotions= ["Sad", "Sad", "Happy", "Fear", "Happy", "Sad"]
        self.assertTrue(emotion in emotions)

    def test_update_emotions(self):
        emotions= ["Sad", "Sad", "Happy", "Fear", "Happy", "Sad"]
        self.assertEqual("Sad", self.analysis_manager.update_emotions(emotions))
        emotions = emotions + ['Happy']
        self.assertTrue("Happy" or "Sad" in self.analysis_manager.update_emotions(emotions))
        emotions = emotions + ['Happy']
        self.assertEqual("Happy", self.analysis_manager.update_emotions(emotions))

    def test_update_todays_sentiment(self):
        claims_len = len(self.analysis_manager.sentiment.claims)
        topics_len = len(self.analysis_manager.sentiment.topics)
        trends_len = len(self.analysis_manager.sentiment.trends)
        self.analysis_manager.todays_sentiment['trends'] = ['lalala']
        self.analysis_manager.todays_sentiment['claims'] = ['lalala']
        self.analysis_manager.todays_sentiment['topics'] = ['lalala']
        self.analysis_manager.update_todays_sentiment(datetime.today())
        self.assertTrue(claims_len < len(self.analysis_manager.sentiment.claims))
        self.assertTrue(topics_len < len(self.analysis_manager.sentiment.topics))
        self.assertTrue(trends_len < len(self.analysis_manager.sentiment.trends))


    def test_get_topic(self):
        trends = {'Donald Trump': AnalysedTrend(1, "Donald Trump", [Claim('claim1', [self.analysed_tweet1, self.analysed_tweet2], 1),
                                   Claim('claim2', [self.analysed_tweet2, self.analysed_tweet3], 2),
                                   Claim('claim3', [self.analysed_tweet1, self.analysed_tweet2], 3),
                                   Claim('claim4', [self.analysed_tweet1, self.analysed_tweet3], 4),
                                   Claim('some claim', [self.analysed_tweet1, self.analysed_tweet2,
                                                        self.analysed_tweet3], 5)])}
        self.analysis_manager.trends_statistics=trends
        for i in range(1,5):
            res = self.analysis_manager.get_topic(i)
            self.assertTrue(len(res)>0)


    def test_get_topics(self):
        trends = {'Donald Trump': AnalysedTrend(1, "Donald Trump",
                                    [AnalysedClaim('claim1', [self.analysed_tweet1, self.analysed_tweet2], 1),
                                   AnalysedClaim('claim2', [self.analysed_tweet2, self.analysed_tweet3], 2),
                                   AnalysedClaim('claim3', [self.analysed_tweet1, self.analysed_tweet2], 3),
                                   AnalysedClaim('claim4', [self.analysed_tweet1, self.analysed_tweet3], 4),
                                   AnalysedClaim('some claim', [self.analysed_tweet1, self.analysed_tweet2,
                                                        self.analysed_tweet3], 5)])}
        self.analysis_manager.trends_statistics=trends
        res = self.analysis_manager.get_topics('Donald Trump')
        self.assertTrue(len(res)>0)

    def test_search_for_emotion_on_tweets(self):
        tweets = self.analysis_manager.search_for_emotion_on_tweets('Sad', self.analysed_tweets)
        self.assertTrue(len(tweets) == 3)

    def test_get_temperature(self):
        self.assertTrue(type(self.analysis_manager.getTemperature())==Temperature)

    def test_calc_avg_prediction(self):
        prediction = {'true': 10, 'fake':10}
        self.assertEqual(0.5, self.analysis_manager.calc_avg_prediction(prediction))

        prediction = {'true': 20, 'fake':0}
        self.assertEqual(1, self.analysis_manager.calc_avg_prediction(prediction))

        prediction = {'true': 0, 'fake':10}
        self.assertEqual(0, self.analysis_manager.calc_avg_prediction(prediction))


    # def test_config_classifier(self):
    #     self.fail()

    # def test_classify_tweets(self):
    #     self.fail()

if __name__ == '__main__':
    unittest.main()
