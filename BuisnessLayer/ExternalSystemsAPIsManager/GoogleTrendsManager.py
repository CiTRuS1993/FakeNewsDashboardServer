from pytrends.request import TrendReq
from PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade import ExternalAPIsORMFacade


class GoogleTrendsManager:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.trends = []
        self.ExternalOrm = ExternalAPIsORMFacade()
        self.connect()


    def connect(self):
        self.trends = {}
        trends = self.pytrends.trending_searches().values.tolist()
        for trend in trends:
            self.trends[self.ExternalOrm.add_trend(trend, "01/03/21")] = {'keywords':trend}

    def get_trends(self):
        return self.trends

