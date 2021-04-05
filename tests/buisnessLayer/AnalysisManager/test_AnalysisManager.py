import time
from unittest import TestCase, mock

from BuisnessLayer.AnalysisManager.AnalysisManager import AnalysisManager
from tests.buisnessLayer.AnalysisManager.TestsObjects import Status, Name, Trend


class TestAnalysisManager(TestCase):

    def setUp(self) -> None:
        self.analysisManager = AnalysisManager()
        self.trends_names = ['Donald Trump', 'Covid19', 'Elections']
        self.trends = {'Donald Trump': Trend(1, 'Donald Trump'), 'Covid19': Trend(2, 'Covid19'),
                       'Elections': Trend(3, 'Elections')}
        self.tweet1 = Status('1', Name('aa'), 'tweet1') # {'id': '1', 'author':'aa', 'content': 'tweet1'}
        self.tweet2 = Status('2', Name('aa'), 'tweet2') # {'id': '2', 'author':'aa', 'content': 'tweet2'}
        self.tweet3 = Status('3', Name('aa'), 'tweet3') # {'id': '3', 'author':'aa', 'content': 'tweet3'}
        self.trends_tweets = {'1':{'id': 1, 'keyword': 'Donald Trump', 'tweets': (self.tweet1, self.tweet2, self.tweet3)}, # 'tweets':{'1': self.tweet1, '2': self.tweet2, '3': self.tweet3}},
                              '2': {'id': 2, 'keyword': 'Covid19', 'tweets': (self.tweet1, self.tweet2, self.tweet3)}, # 'tweets':{'1': self.tweet1, '2': self.tweet2, '3': self.tweet3}},
                              '3': {'id': 3, 'keyword': 'Elections', 'tweets': (self.tweet1, self.tweet2, self.tweet3)}} # 'tweets':{'1': self.tweet1, '2': self.tweet2, '3': self.tweet3}}}
        self.claims = ['claim1', 'claim2', 'claim3']
        self.snopes = {'claim1': [self.tweet1, self.tweet2, self.tweet3],
                       'claim2': [self.tweet1, self.tweet2, self.tweet3],
                       'claim3': [self.tweet1, self.tweet2, self.tweet3]}

    # TODO
    # # @patch("BuisnessLayer.AnalysisManager.addTrend")
    # # @patch("")
    # def test_classify_trends(self):
    #     # mock_add_trend = Mock.mock()
    #     self.assertEqual({}, self.analysisManager.getGoogleTrendsStatistics())
    #     # amount = len(self.analysisManager.dashboard_statistics.keys())
    #     self.assertTrue(self.analysisManager.classifyTrends(self.trends_tweets))
    #     time.sleep(10)
    #     # print(self.analysisManager.getGoogleTrendsStatistics())
    #     self.assertTrue(len(self.analysisManager.getGoogleTrendsStatistics().keys()) > 0)
    #     # self.assertTrue(len(self.analysisManager.dashboard_statistics()) > amount)

    # TODO
    # def test_classify_snopes(self):
    #     self.assertEqual({}, self.analysisManager.getSnopesStatistics())
    #     # amount = len(self.analysisManager.dashboard_statistics())
    #     self.analysisManager.classifySnopes(self.snopes)
    #     time.sleep(10)
    #     self.assertTrue(len(self.analysisManager.getSnopesStatistics()) > 0)
    #     # self.assertTrue(len(self.analysisManager.dashboard_statistics()) > amount)

    @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_get_claims_from_trend(self, mock_claims):
        ret = {}
        for trend in self.trends_names:
            ret[trend] = self.claims
        mock_claims.get_claims_from_trend.return_value = ret
        for trend in self.trends_tweets:
            claims = self.analysisManager.get_claims_from_trend(self.trends_tweets[trend]['tweets'])
            self.assertTrue(len(claims) > 0)
            for claim in claims:
                assert claim.name in self.claims

    # @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_add_new_trends_statistics(self, mock_claims):
        self.fail()

    # @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_init_trend_statistics(self, mock_claims):
        self.fail()

    # @mock.patch("BuisnessLayer.AnalysisManager.ClassifierAdapter")
    def test_calc_topics_statistics_and_save(self, mock_claims):
        self.fail()

    def test_get_trend_name(self):
        self.analysisManager.trends_statistics = {'1': Trend(1, 'Donald Trump'), '2': Trend(2, 'Covid19'),
                                                  '3': Trend(3, 'Elections')}
        self.analysisManager.trends = self.trends
        assert self.analysisManager.get_trend_name('1') == 'Donald Trump'
        assert self.analysisManager.get_trend_name('2') == 'Covid19'
        assert self.analysisManager.get_trend_name('3') == 'Elections'

    def test_get_tweets_by_emotion(self):
        self.analysisManager.classifyTrends(self.trends_tweets)
        time.sleep(10)
        emotion = self.analysisManager.getGoogleTrendsStatistics()['Donald Trump']['statistics']['emotion'][0]
        # print(emotion)
        # print(self.analysisManager.get_emotion_tweets(emotion))
        self.assertTrue(len(self.analysisManager.get_emotion_tweets(emotion))>0)

    def test_update_emotions(self):
        self.fail()

    def test_update_todays_sentiment(self):
        self.fail()

    def test_addTrend(self):
        self.fail()

    def test_get_topic(self):
        self.fail()

    def test_search_for_emotion_on_tweets(self):
        self.fail()

    def test_classify_tweets(self):
        self.fail()

    def test_config_classifier(self):
        self.fail()