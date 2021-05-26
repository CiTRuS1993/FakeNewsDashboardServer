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
            if trend[0] not in self.all_trends.keys():
                t_id = self.ExternalOrm.add_trend(trend[0], str(date))
                self.trends[t_id] = {'keywords': trend[0]} # was trend instead of trend[0]
                self.all_trends[trend[0]] = self.ExternalOrm.get_trend(t_id).copy()
            else:
                flag = False
                for trend_dict in self.all_trends[trend[0]]:
                    # print(trend_dict['date'])
                    if type(trend_dict) == str:
                        trend_date = trend_dict
                    else:
                        trend_date = trend_dict['date']
                    if self.compare_dates(trend_date, date) == 0:
                    # if trend_dict['date'] == str(date):
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

    def compare_dates(self, date1, date2):
        if type(date1) is str:
            if '-' in date1:
                date1 = datetime(int(date1[:4]), int(date1[5:7]), int(date1[8:])).date()
            else:
                date1 = datetime(int("20"+date1[6:]), int(date1[3:5]), int(date1[:2])).date()
        if date1.year != date2.year:
            if date1.year > date2.year:
                return 1
            else:
                return -1
        elif date1.month != date2.month:
            if date1.month > date2.month:
                return 1
            else:
                return -1
        elif date1.day == date2.day:
            return 0
        elif date1.day > date2.day:
            return 1
        else:
            return -1