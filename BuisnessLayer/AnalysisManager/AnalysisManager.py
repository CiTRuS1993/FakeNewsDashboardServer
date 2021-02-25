import threading

from BuisnessLayer.AnalysisManager.ClassifierAdapter import ClassifierAdapter

# trend -> topics
# snopes claims
# on each one -> sentiment [-3,3], emotional, fake
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

    # TODO
    def classifyTweets(self, file):
        # read file
        # self.adapter.analyze(data, callback)
        pass

    def retrieveFakeNewsData(self):
        return self.dashboard_statistics

    # TODO
    def configClassifier(self, classifier, configuration):
        pass

    def classifyTrends(self, trends):
        def callback(processed):
            self.dashboard_statistics = processed # Yarin- maybe =+ instead of =

        fail = False
        claims = {}
        for trend in trends:
            claims[trend] = self.get_claims_from_trend(trend)
            # if returns wrong output -> fail = True
        analyze_thread = threading.Thread(target=self.adapter.analyze, args=(trends, callback)) # TODO- send claims instead of trends on args
        analyze_thread.start()
        return not fail

    def classifySnopes(self, claims):
        # def callback(processed):
        #     self.dashboard_statistics += processed # Yarin- maybe = instead of =+
        #
        # for claim in claims:
        #     tweets = retrieve_tweets(claim)   ??????
        #     analyze_thread = threading.Thread(target=self.adapter.analyze,args=(tweets, callback))
        #     analyze_thread.start()
        pass

    # send the tweets of some trend to the claims classifier and return its answer (claims)
    def get_claims_from_trend(self, trends_tweets):
        return self.adapter.get_claims_from_trend(trends_tweets)
