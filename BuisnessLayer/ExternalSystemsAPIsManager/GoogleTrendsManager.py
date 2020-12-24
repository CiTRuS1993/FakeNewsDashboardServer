from pytrends.request import TrendReq


class GoogleTrendsManager:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.trends = []
        self.connect()

    def connect(self):
        self.trends = self.pytrends.trending_searches().values.tolist()

    def get_trends(self):
        return self.trends
