from unittest import TestCase

import pandas as pd

from BuisnessLayer.ExternalSystemsAPIsManager.GoogleTrendsManager import GoogleTrendsManager
from unittest import mock

# from PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade import ExternalAPIsORMFacade


class TestGoogleTrendsManager(TestCase):
    # def setUp(self) -> None:
    #     self.googleTrendsManager = GoogleTrendsManager()
    @mock.patch('BuisnessLayer.ExternalSystemsAPIsManager.GoogleTrendsManager.TrendReq.trending_searches',
                return_value=pd.DataFrame(["s"]))
    @mock.patch('BuisnessLayer.ExternalSystemsAPIsManager.GoogleTrendsManager.ExternalAPIsORMFacade')
    def test_connect(self, mocks, trend):
        mocks.get_all_trends.return_value = []
        mocks.get_trend.return_value = "s"
        self.googleTrendsManager = GoogleTrendsManager()
        trend.trending_searches.return_value = ["s"]
        assert len(self.googleTrendsManager.get_trends()) >= 1
