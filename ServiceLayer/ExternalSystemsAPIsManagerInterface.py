from BuisnessLayer.ExternalSystemsAPIsManager.ExternalSystemsFacade import ExternalSystemsFacade

class ExternalSystemsAPIsManagerInterface:

    def __init__(self):
        self.extrenalManagerLogic=ExternalSystemsFacade()
        # timer

    def searchTweetsByKeywords(self, keyword, token):
        return self.extrenalManagerLogic.search_tweets_by_keywords(keyword, token)

    def retrieveGoogleTrendsData(self):
        return self.extrenalManagerLogic.retrieve_google_trends_data()

    def retrieveSnopesData(self):
        return self.extrenalManagerLogic.retrieve_snopes_data()

    # tokens is list of strings
    def editTwittersTokens(self, tokens):
        return self.extrenalManagerLogic.edit_twitters_tokens(tokens)


    def search_for_empty_trends(self, empty_trends):
        trend = {}
        for (trend_id, keywords) in empty_trends:
            print("at search_for_empty_trends, should search for trend={keywords} with id={trend_id}")
            # TODO