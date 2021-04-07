from unittest import TestCase, mock

from ServiceLayer.AnalysisManagerInterface import AnalysisManagerInterface
from tests.buisnessLayer.AnalysisManager.TestsObjects import Status, Name, Trend, AnalysedTweet


class TestAnalysisManagerInterface(TestCase):
    def setUp(self) -> None:
        self.analysisManager = AnalysisManagerInterface()
        self.trends_names = ['Donald Trump', 'Covid19', 'Elections']
        self.trends = {'Donald Trump': Trend(1, 'Donald Trump'), 'Covid19': Trend(2, 'Covid19'),
                       'Elections': Trend(3, 'Elections')}
        self.tweet1 = Status('1', Name('aa'), 'tweet1')
        self.tweet2 = Status('2', Name('aa'), 'tweet2')
        self.tweet3 = Status('3', Name('aa'), 'tweet3')
        self.trends_tweets = {
            '1': {'id': 1, 'keyword': 'Donald Trump', 'tweets': (self.tweet1, self.tweet2, self.tweet3)},
            '2': {'id': 2, 'keyword': 'Covid19', 'tweets': (self.tweet1, self.tweet2, self.tweet3)},
            '3': {'id': 3, 'keyword': 'Elections', 'tweets': (self.tweet1, self.tweet2,
                                                              self.tweet3)}}
        self.claims = ['claim1', 'claim2', 'claim3']
        self.snopes = {'claim1': set(['tweet1', 'tweet2','tweet3']),
                       'claim2': set(['tweet1', 'tweet2','tweet3']),
                       'claim3': set(['tweet1', 'tweet2','tweet3'])}
        self.analysed_tweets = {}
        self.analysed_tweet1 = AnalysedTweet('1', Name('aa'), 'tweet1', 'happy', 2, '0')
        self.analysed_tweet2 = AnalysedTweet('2', Name('aa'), 'tweet2', 'sad', -1, '1')
        self.analysed_tweet3 = AnalysedTweet('3', Name('aa'), 'tweet3', 'sad', -3, '0')
        self.analysed_tweets = {
            '1': {'id': 1, 'keyword': 'Donald Trump',
                  'tweets': (self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3)},
            '2': {'id': 2, 'keyword': 'Covid19',
                  'tweets': (self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3)},
            '3': {'id': 3, 'keyword': 'Elections',
                  'tweets': (self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3)}}
        self.temp = [] # TODO- create temp objects
        self.emotions = [] # TODO- create emotions objects
        self.sentiment = [] # TODO- create sentiment objects


    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_classify_trends(self, mock):
        self.analysisManager.analysisManagerLogic= mock
        mock.classifyTrends.return_value = []
        mock.getGoogleTrendsStatistics.return_value = self.analysed_tweets
        self.assertEqual(self.analysisManager.classifyTrends(self.trends_tweets), self.analysed_tweets)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_classify_snopes(self, mock):
        self.analysisManager.analysisManagerLogic= mock
        mock.classifySnopes.return_value = []
        mock.getSnopesStatistics.return_value = self.analysed_tweets
        self.assertEqual(self.analysisManager.classifySnopes(self.snopes), self.analysed_tweets)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_classify_tweets(self, mock):
        self.analysisManager.analysisManagerLogic = mock
        mock.classifyTweets.return_value = self.analysed_tweets
        self.assertEqual(self.analysisManager.classifyTweets('file_dir'), self.analysed_tweets)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_config_classifier(self, mock):
        self.analysisManager.analysisManagerLogic = mock
        ret = ['TODO']
        mock.configClassifier.return_value = ret
        self.assertEqual(self.analysisManager.configClassifier('classifier1', 'config'), ret)

# TODO- wasn't implemented yet
    # def test_tag_tweets(self):
    #     self.fail()

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_Google_Trends_statistics(self, mock):
        self.analysisManager.analysisManagerLogic = mock
        ret = self.analysed_tweets
        mock.getGoogleTrendsStatistics.return_value = ret
        self.assertEqual(self.analysisManager.getGoogleTrendsStatistics(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_Snopes_statistics(self, mock):
        self.analysisManager.analysisManagerLogic = mock
        ret = self.snopes
        mock.getSnopesStatistics.return_value = ret
        self.assertEqual(self.analysisManager.getSnopesStatistics(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_retrieve_fake_news_data(self, mock):
        self.analysisManager.analysisManagerLogic = mock
        ret = {'todo': 'do we need it?????'}
        mock.retrieveFakeNewsData.return_value = ret
        self.assertEqual(self.analysisManager.retrieveFakeNewsData(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_temperature(self, mock):
        self.analysisManager.analysisManagerLogic = mock
        ret = self.temp
        mock.getTemperature.return_value = ret
        self.assertEqual(self.analysisManager.getTemperature(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_emotions(self, mock):
        self.analysisManager.analysisManagerLogic = mock
        ret = self.emotions
        mock.get_emotions.return_value = ret
        self.assertEqual(self.analysisManager.get_emotions(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_sentiment(self, mock):
        self.analysisManager.analysisManagerLogic = mock
        ret = self.sentiment
        mock.get_sentiment.return_value = ret
        self.assertEqual(self.analysisManager.get_sentiment(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_topic(self, mock):
        self.analysisManager.analysisManagerLogic = mock
        ret = self.trends_tweets['1']
        mock.get_topic.return_value = ret
        self.assertEqual(self.analysisManager.get_topic(1), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_emotion_tweets(self, mock):
        self.analysisManager.analysisManagerLogic = mock
        ret = self.analysed_tweets
        mock.get_emotion_tweets.return_value = ret
        self.assertEqual(self.analysisManager.get_emotion_tweets('happy'), ret)