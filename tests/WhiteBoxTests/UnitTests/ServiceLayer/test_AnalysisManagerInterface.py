import unittest
from unittest import mock

from ServiceLayer.AnalysisManagerInterface import AnalysisManagerInterface
from tests.WhiteBoxTests.UnitTests.buisnessLayer.AnalysisManager import AnalysedTweet, Name, Status


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.analysis_manager= AnalysisManagerInterface()
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
        self.temp = []
        self.emotions = []
        self.sentiment = []
        self.tweet1 = Status('1', Name('aa'), 'tweet1')
        self.tweet2 = Status('2', Name('aa'), 'tweet2')
        self.tweet3 = Status('3', Name('aa'), 'tweet3')
        self.trends_tweets = {
            '1': {'id': 1, 'keyword': 'Donald Trump', 'tweets': (self.tweet1, self.tweet2, self.tweet3)},
            '2': {'id': 2, 'keyword': 'Covid19', 'tweets': (self.tweet1, self.tweet2, self.tweet3)},
            '3': {'id': 3, 'keyword': 'Elections', 'tweets': (self.tweet1, self.tweet2,
                                                              self.tweet3)}}

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_getGoogleTrendsStatistics(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        ret = self.analysed_tweets
        mock.getGoogleTrendsStatistics.return_value = ret
        self.assertEqual(self.analysis_manager.getGoogleTrendsStatistics(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_getSnopesStatistics(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        ret = self.snopes
        mock.getSnopesStatistics.return_value = ret
        self.assertEqual(self.analysis_manager.getSnopesStatistics(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_classifyTweets(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        ret = {'TODO': 'why am I doing it???'}
        mock.classifyTweets.return_value = ret
        self.assertEqual(self.analysis_manager.classifyTweets('file_dir'), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_retrieveFakeNewsData(self, mock_analysis):  # returns statistics
        self.analysis_manager.analysisManagerLogic = mock_analysis
        ret = {'TODO': 'why am I doing it???'}
        mock_analysis.retrieveFakeNewsData.return_value = ret
        self.assertEqual(self.analysis_manager.retrieveFakeNewsData(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_configClassifier(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        ret = True
        mock.configClassifier.return_value = ret
        self.assertEqual(self.analysis_manager.configClassifier('classifier1', 'configuration'), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_classifyTrends(self, mock):  # returns statistics
        self.analysis_manager.analysisManagerLogic = mock
        ret = self.analysed_tweets
        mock.getGoogleTrendsStatistics.return_value = ret
        self.assertEqual(self.analysis_manager.classifyTrends(self.trends_tweets), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_classifySnopes(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        ret = self.analysed_tweets
        mock.getSnopesStatistics.return_value = ret
        self.assertEqual(self.analysis_manager.classifySnopes(self.snopes), ret)

    # @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    # def test_tagTweets(self):
    #     self.analysis_manager.analysisManagerLogic = mock
    #     ret = self.analysed_tweets
    #     mock.tagTweets.return_value = ret
    #     self.assertEqual(self.analysis_manager.tagTweets('2323', '1'), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_getTemperature(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        ret = self.temp
        mock.getTemperature.return_value = ret
        self.assertEqual(self.analysis_manager.getTemperature(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_emotions(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        ret = self.emotions
        mock.get_emotions.return_value = ret
        self.assertEqual(self.analysis_manager.get_emotions(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_sentiment(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        ret = self.sentiment
        mock.get_sentiment.return_value = ret
        self.assertEqual(self.analysis_manager.get_sentiment(), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_topic(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        ret = {'tweets': self.analysed_tweets, 'emotions': self.emotions}
        mock.get_topic.return_value = ret
        self.assertEqual(self.analysis_manager.get_topic(1), ret)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_emotion_tweets(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        ret = self.analysed_tweets
        mock.get_emotion_tweets.return_value = ret
        self.assertEqual(self.analysis_manager.get_emotion_tweets('happy'), ret)

if __name__ == '__main__':
    unittest.main()
