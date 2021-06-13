
import threading
from dataclasses import asdict
from datetime import datetime
from threading import Lock
import schedule

from BuisnessLayer.AnalysisManager.ClassifierAdapter import ClassifierAdapter
from BuisnessLayer.AnalysisManager.DataObjects import *
from PersistenceLayer.AnalysisORM.AnalysisORMFacade import AnalysisORMFacade


class AnalysisManager:

    def __init__(self):
        self.trends = {}
        self.lock = Lock()
        self.todays_sentiment = {'trends': 0, 'topics': 0, 'claims': 0}
        self.emotions = self.init_emotions_dict()
        # self.emotion_tweets = {"Anger":list(), "Disgust": list(), "Sad":list(), "Happy": list(), "Surprise": list(), "Fear": list()}
        self.temperature = {'sentiment': 0, 'is_fake': 0, 'amount': 1}
        # self.dashboard_statistics = {}
        self.trends_statistics = {}
        self.snopes_statistics = {}
        self.adapter = ClassifierAdapter()

        # retrieve previous analysis's from DB
        self.orm = AnalysisORMFacade()
        self.orm_trends = self.orm.get_all_trends()
        self.orm_topics = self.orm.get_all_analyzed_topics()
        # self.orm_claims = self.orm.get_all_analyzed_claims() # TODO- uncomment
        self.orm_tweets = self.orm.get_all_analyzed_tweets()

        self.retrieveFakeNewsDataFromDB()
        self.sentiment = self.retrieve_sentiment()

        schedule.every().day.at("23:57").do(lambda: (self.update_todays_sentiment(datetime.date.today())))

    def init_emotions_dict(self):
        return {'emotions': [
            {'amount': 1, 'label': "Angry"},
            {'amount': 1, 'label': "Sad"},
            {'amount': 1, 'label': "Happy"},
            {'amount': 1, 'label': "Surprise"},
            {'amount': 1, 'label': "Fear"}
        ]}

    # should return dict of <trend name> : TrendStatistics asdict --> asdict(trend.statistics)
    def getGoogleTrendsStatistics(self):
        # print(self.trends_statistics)
        current_statistics = dict()
        for trend in self.trends_statistics:
            current_statistics[self.get_trend_name(trend, self.trends_statistics[trend])] = \
                asdict(self.trends_statistics[trend].statistics)
        return current_statistics

    def getSnopesStatistics(self):
        return self.snopes_statistics

    def classifyTweets(self, file):
        # read file
        # self.adapter.analyze(data, callback)
        # save to DB
        return False

    def retrieveFakeNewsData(self):
        return self.dashboard_statistics

    def configClassifier(self, classifier, configuration):
        pass

    def add_new_trends_statistics(self, processed, trends_dict,res):
        for trend_id in processed.keys():  # processed is type of dict<trend name> = list <Claim>
            # print(f"add_new_trends_statistics:")
            # print(f"processed = {processed}")
            # print(f"trends_dict = {trends_dict}")
            topics_statistics = list()
            trend_name = self.get_trend_name(trend_id, trends_dict)
            words_cloud, topics_statistics= self.calc_topics_statistics_and_save(processed, topics_statistics, trend_id,res)
            # -------------------- sync ----------------------- (was fixed by wait() on tests)
            self.lock.acquire()
            if trend_id not in self.trends_statistics.keys():
                first = True
                for (emotions, sentiment, prediction) in topics_statistics:
                    if first and len(emotions) > 0:
                        first = False
                        trend_statistics = self.init_trend_statistics(emotions, prediction, sentiment, words_cloud)
                        self.trends_statistics[trend_id] = AnalysedTrend(trend_id, trend_name, processed[trend_id],
                                                                         trend_statistics)
                    else:
                        try:
                            self.trends_statistics[trend_id].statistics.statistics.add_statistics(emotions, sentiment,
                                                                                                  prediction)
                            # self.addTrend(self.trends_statistics[trend_id]) # delete?
                        except:
                            trend_statistics = self.init_trend_statistics(emotions, prediction, 17*(sentiment+3), words_cloud)
                            self.trends_statistics[trend_id] = AnalysedTrend(trend_id, trend_name, processed[trend_id],
                                                                             trend_statistics)
                self.lock.release()
            # --------------------- until here ---------------------
        return len(topics_statistics)

    def init_trend_statistics(self, emotions, prediction, sentiment, words_cloud):
        if type(emotions) != str:
            emotion = self.update_emotions(emotions)
        else:
            print(f"at init_trend_statistics, emotions should be list but its = {emotions}")
            emotion= emotions
        avg_prediction = self.calc_avg_prediction(prediction)
        if len(emotions) > 0:
            trend_sentiment = sentiment / len(emotions)
        else:
            trend_sentiment = sentiment
        statistics = Statistics(emotion, trend_sentiment, avg_prediction, len(emotions))
        print(f"at init_trend_statistics, trend statistics = {statistics}")
        # statistics = Statistics(emotion, trend_sentiment, avg_prediction, 50, len(emotions))
        trend_statistics = TrendStatistic(words_cloud, statistics)
        return trend_statistics

    def calc_topics_statistics_and_save(self, processed, topics_statistics, trend,res):
        print("at calc_topics_statistics_and_save")
        words_cloud = dict()
        # topics_statistics= list() # format : (emotions, sentiment, prediction)
        for topic in processed[trend]:
            prediction = {'true': 0, 'fake': 0}
            emotions = list()
            sentiment = 0
            ids = []
            for tweet in topic.tweets:
                for word in tweet.content.split():
                    if word in words_cloud:
                        words_cloud[word] = words_cloud[word] + 1
                    else:
                        words_cloud[word] = 1
                ids.append(tweet.id)
                sentiment = sentiment + tweet.sentiment

                prediction[tweet.is_fake] = prediction[tweet.is_fake] + 1
                emotions.append(tweet.emotion)
                # TODO- if fails on the way --> delete the analysis?
                if tweet.id not in self.orm_tweets.keys():
                    self.orm.add_analyzed_tweet(tweet.id, tweet.is_fake, tweet.emotion, tweet.sentiment)
                    # self.orm_tweets[tweet.id] = self.orm.get_analyzed_tweet(tweet.id)
            # update emotions statistics
            emotion = self.update_emotions(emotions)
            avg_prediction = self.calc_avg_prediction(prediction)
            topics_statistics.append((emotions, sentiment, prediction)) # maybe avg_sentiment
            avg_sentiment = sentiment
            if len(emotions)>0:
                avg_sentiment= sentiment / len(emotions)
            print(f"try to save the analysed topic '{topic.name}'")
            topic_id = self.orm.add_analyzed_topic(topic.name, avg_prediction, emotion, avg_sentiment, ids, trend)
            while (not topic_id):
                print(f"try to save the analysed topic '{topic.name}'")
                topic_id = self.orm.add_analyzed_topic(topic.name, avg_prediction, emotion, avg_sentiment, ids, trend)
            topic.setID(topic_id)
            self.orm.update_topic(topic.id,topic.name,res[res['author_guid']==topic.id]['pred'].values[0], emotion, avg_sentiment)
            topics_statistics.append((emotion, avg_sentiment, avg_prediction))
            print(topic_id)
        words_cloud_statistics = list()
        for word in words_cloud.keys():
            words_cloud_statistics.append(WordCloud(word, words_cloud[word]))
        self.update_orm_tweets()
        return words_cloud_statistics, topics_statistics

    # TODO- make this func shorter
    def get_trend_name(self, trend_id, trends_dict):
        # print(f"trend id is {trend_id}")
        not_found = True
        trend_name = ''
        for analysed_trend_id in self.trends_statistics:
            if analysed_trend_id == trend_id:
                not_found = False
                trend_name = self.trends_statistics[analysed_trend_id].keywords
        if not_found:
            for keywords in self.trends:
                if trend_id == self.trends[keywords].id:
                    trend_name = keywords
                    not_found = False
        if not_found:
            for trend_db in self.orm_trends.keys():
                if self.orm_trends[trend_db]['id'] == trend_id:
                    trend_name = trend_db
                    not_found = False
        if not_found:
            if trend_id in trends_dict.keys():
                trend = trends_dict[trend_id]
                trend_name = trend.keywords
                not_found = False
        if not_found:
            print("problem in BL.AnalysisManager.get_trend_name()")
        return trend_name

    def classifyTrends(self, trends_tweets):
        trends = {}
        empty_trends = []
        for trend_id in trends_tweets:
            empty_trend= False
            print("trend:{}".format(trend_id))
            if len(trends_tweets[trend_id]['tweets'])==0:
                print("empty trend {}".format(trend_id))
                empty_trend= True
                empty_trends.append((trend_id, trends_tweets[trend_id]['keyword']))
                continue
            claims = self.get_claims_from_trend(trends_tweets[trend_id]['tweets'][0:1000])  # <trend_name> : list <Claim>
            print("num of claims:{}".format(len(claims)))
            for claim in claims:
                claim.id = self.orm.add_analyzed_topic(claim.name,None,None,0,list(map(lambda t: t.id,claim.tweets)),trend_id)
            print("topics added to db")
           
            trend = Trend(trend_id, trends_tweets[trend_id]['keyword'], claims)
            trends[trend_id] = trend
            
                
            # self.addTrend(trend)
            # print('trend keyword= ' + trends_tweets[trend_id]['keyword'])
        # print("trends:")
        # print(trends)
        analyze_thread = threading.Thread(target=self.adapter.analyze_trends,
                                          args=(trends, self.add_new_trends_statistics))
        analyze_thread.start()
        return empty_trends

    def classifySnopes(self, claims_tweets):
        def callback(processed):
            # calculate the claims statistics
            sentiment = 0
            prediction = {'true': 0, 'fake': 0}
            emotions = list()
            for claim in processed.keys():
                for tweet in processed[claim].tweets:
                    self.orm.add_analyzed_tweet(tweet.id, tweet.is_fake, tweet.emotion, tweet.sentiment)
                    emotions.append(tweet.emotion)
                    prediction[tweet.is_fake] = prediction[tweet.is_fake] + 1
                    sentiment = sentiment + tweet.sentiment
                # update emotions statistics
                emotion = self.update_emotions(emotions)
                avg_prediction = self.calc_avg_prediction(prediction)
                if len(emotions) > 0:
                    avg_sentiment = sentiment / len(emotions)
                else:
                    avg_sentiment = sentiment
                # save the new claims to DB
                # self.orm.add_analyzed_claim(claim.name, avg_prediction, emotion, avg_sentiment)   TODO - uncomment and name is instead of id
                # update statistics to display the new analyzed data
                # if claim in self.snopes_statistics:
                self.lock.acquire()
                try:
                    self.snopes_statistics[claim].add_statistics(emotions, sentiment, prediction)
                # else:
                except:
                    statistics = Statistics(emotion[0], avg_sentiment, avg_prediction, len(emotions))
                    # statistics = Statistics(emotion[0], avg_sentiment, avg_prediction, 15, len(emotions))
                    analysed_claim = AnalysedClaim(claim, processed[claim].tweets, statistics)
                    self.snopes_statistics[claim] = analysed_claim
                self.lock.release()
            return True

        # apply analyze concurrently on each new Snopes claim
        analyze_thread = threading.Thread(target=self.adapter.analyze_snopes, args=(claims_tweets, callback))
        analyze_thread.start()

    # send the tweets of some trend to the claims classifier and return its answer (claims)
    # initialize the data structures : Claim, Tweet
    # returns list <Claim>
    def get_claims_from_trend(self, trends_tweets):
        claims = self.adapter._get_claim_from_trend(trends_tweets)
        # claims = list()
        # for key in claims_dict.keys():
        #     tweets = list()
        #     for tweet_id in claims_dict[key]:
        #         tweets.append(Tweet(tweet_id, claims_dict[key][tweet_id]['author'],
        #                             claims_dict[key][tweet_id]['content']))  # tweet = id, author, content
        #     claim = Claim(key, tweets,0) #todo :id
        #     claims.append(claim)

        #   YARIN 11/06:
        # claims_dict = self.adapter.get_claims_from_trend(trends_tweets)
        # claims = list()
        # for key in claims_dict.keys():
        #     tweets = list()
        #     for tweet_id in claims_dict[key]:
        #         tweets.append(Tweet(tweet_id, claims_dict[key][tweet_id]['author'],
        #                             claims_dict[key][tweet_id]['content']))  # tweet = id, author, content
        #     claim = Claim(key, tweets, 0)
        #     claims.append(claim)
        return claims

    def getTemperature(self):
        is_fake = self.temperature['is_fake'] / self.temperature['amount']
        if is_fake < 0.5:
            is_fake = 0
        else:
            is_fake = 1
        temperature = Temperature(
            #self.temperature['authenticity'],
                                  round(self.temperature['sentiment'] / self.temperature['amount']),
                                  is_fake)
        return temperature

    def get_emotions(self):
        # print(f"emotions: {self.emotions}")
        return self.emotions

    def update_emotions(self, emotions):
        # calculate the most repetitive emotion
        emotions_counter = {"Angry": 0, "Sad": 0, "Happy": 0, "Surprise": 0, "Fear": 0}
        for emotion in emotions:
            emotions_counter[emotion] = emotions_counter[emotion] + 1
        max_emotion_counter = max([emotions_counter[emotion] for emotion in emotions_counter])
        max_emotion = [emotion for emotion in emotions_counter if emotions_counter[emotion] == max_emotion_counter]
        # update the emotions statistics
        for emotion_dict in self.emotions['emotions']:
            emotion_dict['amount'] = emotion_dict['amount'] + emotions_counter[emotion_dict['label']]
        return max_emotion[0]

    def calc_avg_prediction(self, prediction):
        try:
            return prediction['true'] / (prediction['true']+prediction['fake'])
        except:
            return 0

    def get_sentiment(self):
        return self.sentiment

    def update_todays_sentiment(self, date):
        todays_trends_sentiment = {'sentiment': self.todays_sentiment['trends'], 'date': str(date)}
        todays_topics_sentiment = {'sentiment': self.todays_sentiment['topics'], 'date': str(date)}
        todays_claims_sentiment = {'sentiment': self.todays_sentiment['claims'], 'date': str(date)}
        self.sentiment.claims.append(todays_claims_sentiment)
        self.sentiment.topics.append(todays_topics_sentiment)
        self.sentiment.trends.append(todays_trends_sentiment)

    # def addTrend(self, trend):
    #     keywords = ""
    #     for k in trend.keywords:
    #         keywords = keywords + k + ' '
    #     # print(trend)
    #     if keywords in self.trends:
    #         print(f"arg trend: {trend.statistics}")
    #         print(f"self trend: {self.trends[keywords].statistics}")
    #         self.trends[keywords].statistics.statistics.copy_statistics(trend.statistics.statistics)
    #     else:
    #         self.trends[keywords] = trend

    def get_topic(self, topic_id):
        # for trend_name in self.trends_statistics:
        #     for topic in self.trends_statistics[trend_name]:
        for trend in self.trends_statistics.keys():
            for topic in self.trends_statistics[trend].claims:
                if topic.id == topic_id:
                    return {'tweets': topic.tweets, 'emotions': topic.get_all_emotions}
        # error case (stub)
        print("Error on AnalysisManager.get_topic()")
        return {'tweets': [{'id': "1361577298282094592", 'emotion': "happy", 'real': "fake", 'sentiment': 3},
                           {'id': "1361577298282094592", 'emotion': "happy", 'real': "true", 'sentiment': -2}],
                'emotions': [{'y': 32, 'label': "Angry"},
                             {'y': 22, 'label': "Disgust"},
                             {'y': 15, 'label': "Sad"},
                             {'y': 19, 'label': "Happy"},
                             {'y': 5, 'label': "Surprise"},
                             {'y': 16, 'label': "Fear"}]}

    def get_emotion_tweets(self, emotion):
        trends_tweets = list()
        snopes_tweets = list()
        for trend in self.trends_statistics:
            for topic in self.trends_statistics[trend].claims:
                trends_tweets = self.search_for_emotion_on_tweets(emotion, topic.tweets)
        for claim in self.snopes_statistics:
            snopes_tweets = self.search_for_emotion_on_tweets(emotion, claim.tweets)
        return trends_tweets + snopes_tweets
        # return {'tweets': [{'id': "1361577298282094592", 'emotion': "happy", 'real': "fake", 'sentiment': 3},
        #                    {'id': "1361577298282094592", 'emotion': "happy", 'real': "true", 'sentiment': 3}]}

    def search_for_emotion_on_tweets(self, emotion, tweets) -> list:
        emotion_tweets = list()
        for tweet in tweets:
            if tweet.emotion == emotion:
                emotion_tweets.append(asdict(tweet))
        return emotion_tweets

    def update_orm_tweets(self):
        self.orm_tweets = self.orm.get_all_analyzed_tweets()

    def retrieveFakeNewsDataFromDB(self):
        today_day = datetime.today().day
        if today_day - 12 > 0:
            date = datetime(datetime.today().year, datetime.today().month, today_day-12).date() # TODO- day-12?
        elif datetime.today().month != 1:
            date = datetime(datetime.today().year, datetime.today().month - 1, 30 - today_day).date()
        else:
            date = datetime(datetime.today().year - 1, 12, 31 - today_day).date()
        trends = self.orm.get_trends_data(date)
        analyzed_trend = {}
        print("trends in db {}".format(len(trends)))
        for trend in trends:
            emotions = []
            prediction = {'true':0,'fake':0}
            sentiment = 0
            words = {}
            print(trend)
            print(len(trends[trend].claims))
            for c in trends[trend].claims:
                print(len(c.tweets))
                for t in c.tweets:
                    for word in t.content.split():
                        if word in words.keys():
                            words[word] = words[word] + 1
                        else:
                            words[word] = 1
                        emotions.append(t.emotion)
                        sentiment+=t.sentiment

                        prediction[t.is_fake] =prediction[t.is_fake] +1

            cloud = []
            for word in words.keys():
                cloud.append(WordCloud(word, words[word]))
            analyzed_trend[trend] = AnalysedTrend(trends[trend].id,trends[trend].keywords,trends[trend].claims,self.init_trend_statistics(emotions,prediction,sentiment,cloud))

        self.trends_statistics = analyzed_trend
        # for

        # trends = {'Sixers': {'date': '2021-05-27', 'id': 2880}, 'Knicks': {'date': '2021-05-27', 'id': 2870},....}
        #
        # for trend_id in processed.keys():  # processed is type of dict<trend name> = list <Claim>
        #     topics_statistics = list()
        #     trend_name = self.get_trend_name(trend_id, trends_dict)
        #     words_cloud = self.calc_topics_statistics_and_save(processed, topics_statistics, trend_id)
        #     if trend_id not in self.trends_statistics.keys():
        #         first = True
        #         for (emotions, sentiment, prediction) in topics_statistics:
        #             if first and len(emotions) > 0:
        #                 first = False
        #                 trend_statistics = self.init_trend_statistics(emotions, prediction, sentiment, words_cloud)
        #                 self.trends_statistics[trend_id] = AnalysedTrend(trend_id, trend_name, processed[trend_id],
        #                                                                  trend_statistics)
        #             else:
        #                 try:
        #                     self.trends_statistics[trend_id].statistics.statistics.add_statistics(emotions, sentiment,
        #                                                                                           prediction)
        #                     # self.addTrend(self.trends_statistics[trend_id]) # delete?
        #                 except:
        #                     trend_statistics = self.init_trend_statistics(emotions, prediction, sentiment, words_cloud)
        #                     self.trends_statistics[trend_id] = AnalysedTrend(trend_id, trend_name, processed[trend_id],
        #                                                                      trend_statistics)

    #   todo
    def retrieve_sentiment(self):
        trend_sentiments = []
        topics_sentiments = []
        for trend in self.trends_statistics.keys():
            print(f"at retrieve_sentiment, trend= {self.trends_statistics[trend]}")
            for topic in self.trends_statistics[trend].claims:
                print(f"at retrieve_sentiment, topic= {topic}")


        # for trend in self.orm_trends:
        #     print(f"on retrieve_sentiment, trend = {trend}")
            # topics= self.orm_trends[trend]
            # for topic in topics:
            #     {'sentiment': topic.statistics.sentiment, 'date':trend}
                
            
        #     try:
        #         print(topic['trend'])
        #     except:
        #         print("no trend")
        # for trend in self.orm_trends:
        #     print(trend)
        #     print(self.orm_trends[trend])
        #     try:
        #         print(self.orm_trends[trend]['trend_topics'])
        #     except:
        #         print("no topic")
        # # topic_sentiments_dict= {}
        # trend_sentiments_dict= {}
        # # topic_sentiments=[]
        # trend_sentiments=[]
        # # for topic in self.orm_topics:
        # #     if topic['date'] in topic_sentiments_dict.keys():
        # #         topic_sentiments_dict[topic['date']]['amount'] = topic_sentiments_dict[topic['date']]['amount']+1
        # #         topic_sentiments_dict[topic['date']]['sentiment'] = topic_sentiments_dict[topic['date']]['sentiment']+topic['sentiment']
        # #     else:
        # #         topic_sentiments_dict.append({topic['date']: {'amount': 1, 'sentiment': topic['sentiment']}})
        # # for date in topic_sentiments_dict.keys():
        # #     topic_sentiments.append({'date': date,
        # #                  'sentiment': topic_sentiments_dict[date]['sentiment']/topic_sentiments_dict[date]['amount']})
        # for trend in self.orm_trends.keys():
        #     date = str(self.orm_trends[trend]['date'])
        #     if date in trend_sentiments_dict.keys():
        #         trend_sentiments_dict[date]['amount'] = trend_sentiments_dict[date]['amount']+1
        #         trend_sentiments_dict[date]['sentiment'] = trend_sentiments_dict[date]['sentiment']+self.orm_trends[trend]['sentiment']
        #     else:
        #         trend_sentiments_dict[date]={'amount': 1, 'sentiment': self.orm_trends[trend]['sentiment']}
        # for date in trend_sentiments_dict.keys():
        #     trend_sentiments.append({'date': date, 'sentiment':
        #                             trend_sentiments_dict[date]['sentiment']/trend_sentiments_dict[date]['amount']})
        # self.sentiment = Sentiment([], trend_sentiments, [])
        # print(self.sentiment)
        # return self.sentiment
        return Sentiment([{'sentiment': 2, 'date': "9.6.2021"}, {'sentiment': 1, 'date': "10.6.2021"},
                                    {'sentiment': 1, 'date': "11.6.2021"}, {'sentiment': 2, 'date': "12.6.2021"},
                                    {'sentiment': 2, 'date': "13.6.2021"}],
                                   [{'sentiment': -1, 'date': "9.6.2021"}, {'sentiment': 0, 'date': "10.6.2021"},
                                    {'sentiment': -1, 'date': "11.6.2021"}, {'sentiment': -2, 'date': "12.6.2021"},
                                    {'sentiment': -2, 'date': "13.6.2021"}],
                                   [{'sentiment': -2, 'date': "9.6.2021"}, {'sentiment': 2, 'date': "10.6.2021"},
                                    {'sentiment': 0, 'date': "11.6.2021"}, {'sentiment': 3, 'date': "12.6.2021"},
                                    {'sentiment': 1, 'date': "13.6.2021"}])

    def get_topics(self, trend_id):
        for trend in self.trends_statistics:
            # print(f"trend_id to search = {trend_id}, curr trend_id={self.trends_statistics[trend].id}")
            # print(f"at get topics, trend (key) on self.trend_statistics={trend}")
            # print(f"all:{self.trends_statistics[trend]}")
            if self.trends_statistics[trend].keywords == trend_id:
                # return {'tweets': self.trends_statistics[trend].claims[0].tweets, 'emotions': self.trends_statistics[trend].claims[0].statistics.emotion}
                # print(f"claims= {self.trends_statistics[trend].claims}")
                # print(f"claims asdict= {asdict(self.trends_statistics[trend].claims)}")
                topics= []
                for topic in self.trends_statistics[trend].claims:
                    words_cloud= self.calc_words_cloud(topic)
                    topic_dict = {'id': topic.id, 'topic':words_cloud, 'statistics': asdict(topic.statistics)}
                    topics.append(topic_dict)
                # print(f"topics = {topics}")
                return topics

    def calc_words_cloud(self, topic):
        words_cloud = dict()
        for tweet in topic.tweets:
            for word in tweet.content.split():
                if word in words_cloud:
                    words_cloud[word] = words_cloud[word] + 1
                else:
                    words_cloud[word] = 1
        words_cloud_statistics = list()
        for word in words_cloud.keys():
            words_cloud_statistics.append(WordCloud(word, words_cloud[word]))
        return words_cloud_statistics