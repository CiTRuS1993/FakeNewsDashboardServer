import threading

from BuisnessLayer.AnalysisManager.ClassifierAdapter import ClassifierAdapter


class AnalysisManager:

    def __init__(self):
        self.dashboard_statistics = {}
        self.trends_statistics = {}
        self.snopes_statistics = {}
        self.adapter = ClassifierAdapter()

    def getGoogleTrendsStatistics(self):
        return self.trends_statistics

    def getSnopesStatistics(self):
        return self.snopes_statistics

    def classifyTweets(self, file):
        pass

    def retrieveFakeNewsData(self):
        return self.dashboard_statistics

    def configClassifier(self, classifier, configuration):
        pass

    def classifyTrends(self, trends):
        def callback(processed):
            self.dashboard_statistics = processed

        analyze_thread = threading.Thread(target=self.adapter.analyze, args=(trends, callback))
        analyze_thread.start()
        return True

    def classifySnopes(self, claims):
        pass
