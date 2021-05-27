from unittest import TestCase

from BuisnessLayer.ExternalSystemsAPIsManager.GoogleTrendsManager import GoogleTrendsManager


class TestGoogleTrendsManager(TestCase):
    def setUp(self) -> None:
        self.googleTrendsManager = GoogleTrendsManager()

    def test_connect(self):
        self.googleTrendsManager.connect()
        assert len(self.googleTrendsManager.get_trends()) > 1
