from ServiceLayer.AnalysisManagerInterface import AnalysisManager
from ServiceLayer.ExternalSystemsAPIsManagerInterface import externalSystemsAPIsManager
from ServiceLayer.UsersManagerInterface import usersManager


class DashboardFacade:

    def __init__(self, username, password):
        self.analysisManager=AnalysisManager()
        self.externalSystemsManager=externalSystemsAPIsManager()
        self.usersManager=usersManager(username, password)


    def retrieveGoogleTrendsData(self):
        pass
    #
    # def initialization(self):
    #     pass
    #
    # def initialization(self):
    #     pass