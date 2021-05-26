from datetime import datetime

from pytrends.request import TrendReq
from PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade import ExternalAPIsORMFacade


class GoogleTrendsManager:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.ExternalOrm = ExternalAPIsORMFacade()
        self.trends = {}
        self.all_trends = self.ExternalOrm.get_all_trends()
        self.connect()


    def connect(self):
        self.trends = {}
        date = datetime.today().date()
        trends = self.pytrends.trending_searches().values.tolist()
        for trend in trends:
            if trend[0] not in self.all_trends.keys(): # TODO- last sql connect
                t_id = self.ExternalOrm.add_trend(trend[0], str(date))
                self.trends[t_id] = {'keywords': trend}
                self.all_trends[trend[0]] = self.ExternalOrm.get_trend(t_id).copy()
            else:
                flag = False
                for trend_dict in self.all_trends[trend[0]]:
                    # print(trend_dict['date'])
                    #WTF
                    if type(trend_dict) is list:
                        trend_dict=trend_dict[0]
                    if trend_dict['date'] == str(date):
                        if trend_dict['id'] not in self.trends and not flag:
                            self.trends[trend_dict['id']] = {'keywords': trend[0]}
                        flag = True


                if not flag:
                    t_id = self.ExternalOrm.add_trend(trend[0], str(date))
                    self.trends[t_id] = {'keywords': trend[0]}
                    self.all_trends[trend[0]].append(self.ExternalOrm.get_trend(t_id).copy())

    def get_trends(self):
        trends = {}
        for trend_name in self.all_trends:
            for trend in self.all_trends[trend_name]:
                if type(trend) is list:
                    trend = trend[0]
                if trend['date'] == str(datetime.today().date()):
                    trends[self.all_trends[trend_name][0]['id']] = {'keywords': trend_name}
        for t_id in self.trends:
            if t_id not in trends.keys():
                trends[t_id] = self.trends[t_id]
        return trends

