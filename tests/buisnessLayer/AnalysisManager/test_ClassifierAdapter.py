from unittest import TestCase

from BuisnessLayer.AnalysisManager.ClassifierAdapter import ClassifierAdapter
from tests.buisnessLayer.AnalysisManager.TestsObjects import Status, Name
from tests.buisnessLayer.AnalysisManager.test_AnalysisManager import TestAnalysisManager


class TestClassifierAdapter(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        setUp = TestAnalysisManager()
        setUp.setUp()
        tweet1 = Status('1', Name('aa'), "RT @girlpilot_: Corona attacks only when I’m in my car alone.So basically I’m protecting me from me. #coronavirus https://t.co/Q8I76rTV…1")  # {'id': '1', 'author':'aa', 'content': 'tweet1'}
        tweet2 = Status('2', Name('aa'), 'RT @swilkinsonbc: Israeli "soldiers" fire through the windscreen of a car, cold-bloodedly shooting &amp; killing a Palestinian man in the head,…')  # {'id': '2', 'author':'aa', 'content': 'tweet2'}
        tweet3 = Status('3', Name('aa'), 'RT @eAsiaMediaHub: FINAL THOUGHT FOR TONIGHT: “You can expect [the U.S.] to continue to speak out strongly &amp; to work with close allies &amp; pa…')  # {'id': '3', 'author':'aa', 'content': 'tweet3'}
        trends_tweets = {
            '1': {'id': 1, 'keyword': 'Donald Trump', 'tweets': (tweet1, tweet2, tweet3)},
            '2': {'id': 2, 'keyword': 'Covid19', 'tweets': (tweet1, tweet2, tweet3)*12},  # '
            '3': {'id': 3, 'keyword': 'Elections', 'tweets': (tweet1, tweet2, tweet3)}}  #
        cls.trend = trends_tweets
        cls.adapter = ClassifierAdapter()
    def test__get_claim_from_trend(self):
        for t in self.trend.keys():
            claim = self.adapter._get_claim_from_trend(self.trend[t]['tweets'])
            print(claim)

