from unittest import TestCase, mock
from

from BuisnessLayer.ExternalSystemsAPIsManager.TwitterManager import TwitterManager
from tests.buisnessLayer.AnalysisManager.TestsObjects import Trend, Name, Status
from PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade import ExternalAPIsORMFacade


class TestTwitterManager(TestCase):

    def setUp(self) -> None:
        self.twitterManager = TwitterManager()
        self.trends_names = ['Donald Trump', 'Covid19', 'Elections']
        self.trends = {'Donald Trump': Trend(1, 'Donald Trump'), 'Covid19': Trend(2, 'Covid19'),
                       'Elections': Trend(3, 'Elections')}
        self.tweet1 = Status('1', Name('aa'), 'tweet1')  # {'id': '1', 'author':'aa', 'content': 'tweet1'}
        self.tweet2 = Status('2', Name('aa'), 'tweet2')  # {'id': '2', 'author':'aa', 'content': 'tweet2'}
        self.tweet3 = Status('3', Name('aa'), 'tweet3')  # {'id': '3', 'author':'aa', 'content': 'tweet3'}
        self.trends_tweets = {
            '1': {'id': 1, 'keyword': 'Donald Trump', 'tweets': (self.tweet1, self.tweet2, self.tweet3)},
            # 'tweets':{'1': self.tweet1, '2': self.tweet2, '3': self.tweet3}},
            '2': {'id': 2, 'keyword': 'Covid19', 'tweets': (self.tweet1, self.tweet2, self.tweet3)},
            # 'tweets':{'1': self.tweet1, '2': self.tweet2, '3': self.tweet3}},
            '3': {'id': 3, 'keyword': 'Elections', 'tweets': (self.tweet1, self.tweet2,
                                                              self.tweet3)}}  # 'tweets':{'1': self.tweet1, '2': self.tweet2, '3': self.tweet3}}}
        self.claims = ['claim1', 'claim2', 'claim3']

    @mock.patch("PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade")
    def test_connect(self,mock):
        self.twitterManager= mock
        self.twitterManager.search_tweets_by_keywords(self,1, keywords, token=None, on_finished=lambda tweets: print(tweets))

    @mock.patch("PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade")
    def test_search_tweets_by_keywords(self,mock):
        self.twitterManager.orm= mock

    def test_stop(self):
        self.fail()

    @mock.patch("BuisnessLayer.TwitterManager")
    def test_search_tweets_by_trends(self,mock):
        self.fail()

    def edit_tokens(self, token):
        for token in token:
            if token not in self.tokens.keys():
                self.tokens.append(token)


    def test_edit_tokens(self):
        self.twitterManager.tokens= {}
        mock.classifyTweets.return_value = self.analysed_tweets
        self.assertEqual(self.analysisManager.classifyTweets('file_dir'), self.analysed_tweets)

    @mock.patch("BuisnessLayer.TwitterManager")
    def test_get_unprocessed_tweets(self):
        self.fail()
