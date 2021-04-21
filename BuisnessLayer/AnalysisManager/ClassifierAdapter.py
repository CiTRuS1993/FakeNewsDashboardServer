import time
from random import random, randint, randrange

from bertopic import BERTopic
import numpy as np
from BuisnessLayer.AnalysisManager.DataObjects import AnalyzedTweet, Claim
import pandas as pd


def get_emotion_by_id(id):
    if id == 1:
        return 'Anger'
    elif id == 2:
        return 'Disgust'
    elif id == 3:
        return 'Sad'
    elif id == 4:
        return 'Happy'
    elif id == 5:
        return 'Surprise'
    else:
        return 'Fear'


# ours, should write also stub
class ClassifierAdapter:
    def __init__(self):
        pass
    def _trends_to_csv(self,trend_dict):
        pass

    def analyze_trends(self, trends_dict, callback):  # trends_dict is type of dict {<trend name> : <Trend>}
        processed_data = {}
        for trend in trends_dict.keys():
            if trend not in processed_data:
                processed_data[trend] = list()
            for topic in trends_dict[trend].claims:
                tweets = list()
                for tweet in topic.tweets:
                    rand = randrange(100)
                    if rand < 50:
                        prediction = "fake"
                    else:
                        prediction = "true"
                    sentiment = randint(-3, 3)
                    rand = randrange(6)
                    emotion = get_emotion_by_id(rand)
                    analyzed_tweet = AnalyzedTweet(tweet.id, tweet.author, tweet.content, emotion, sentiment,
                                                   prediction)
                    tweets.append(analyzed_tweet)
                processed_data[trend].append(Claim(topic, tweets))

        time.sleep(1)
        return callback(processed_data)

    def analyze_snopes(self, data, callback):  # data is type of dict {<claim name> : list <tweets>}
        # print(data)
        # processed_data = {}
        # for key in data.keys():
        #     if key not in processed_data:
        #         processed_data[key]={}
        #     for tweet in data[key].keys():
        #         processed_data[key][tweet]={}
        #         rand = randrange(100)
        #         if rand < 50:
        #             processed_data[key][tweet]['prediction'] = "wow it's fake"
        #         else:
        #             processed_data[key][tweet]['prediction'] = "100% true"
        #         sentiment = randint(-3, 3)
        #         processed_data[key][tweet]['sentiment'] = sentiment
        #         rand = randrange(6)
        #         processed_data[key][tweet]['emotional'] = get_emotion_by_id(rand)

        processed_data = {}
        for claim in data.keys():
            # if claim not in processed_data:
            #     processed_data[claim]= list()
            tweets = list()
            for tweet in data[claim]:
                rand = randrange(100)
                if rand < 50:
                    prediction = "fake"
                else:
                    prediction = "true"
                sentiment = randint(-3, 3)
                rand = randrange(6)
                emotion = get_emotion_by_id(rand)

                analyzed_tweet = AnalyzedTweet(tweet['id'], tweet['author'], tweet['content'], emotion, sentiment,
                                               prediction)
                tweets.append(analyzed_tweet)
            if claim in processed_data.keys():
                processed_data[claim].append(Claim(claim, tweets))
            else:
                processed_data[claim] = Claim(claim, tweets)

        time.sleep(1)
        return callback(processed_data)

    def get_claims_from_trend(self, trends_tweets):
        claims = {'claim1': {}, 'claim2': {}}
        for status in trends_tweets:
            rand = randrange(10)
            # print(status.id)
            # print(status.text)
            # print(status.author.name)
            if rand < 5:
                claims["claim1"][status.id] = {'id': status.id, 'author': status.author.name, 'content': status.text}
            else:
                # print(status)
                claims["claim2"][status.id] = {'id': status.id, 'author': status.author.name, 'content': status.text}
        return claims

    def _get_claim_from_trend(self, trends_tweets):
        df = pd.DataFrame([tweet.__dict__ for tweet in trends_tweets])[['id', 'text']]
        if len(df)<15:
            from collections import Counter
            claim_text = ' '.join([txt[0] for txt in Counter(" ".join(df['text'].str.replace("RT", '').values).split(' ')).most_common(10)])
            return [Claim(claim_text,df['id'].values)]
        bt = BERTopic()

        topics = bt.fit_transform(df['text'].str.replace("RT", '').values)
        df['topic_id'] = topics[0]
        topic_info = bt.get_topics()
        topics_text = {}
        for key in topic_info.keys():
            lst = topic_info[key]

            topics_text[key] = ' '.join([x[0] for x in lst])

        # df['topic_text'] = df['topic_id'].apply(lambda x:topics_text[x])
        claims = []
        for t in topic_info.keys():
            tweets = df[df['topic_id'] == t]['id'].values
            claims.append(Claim(topics_text[t], tweets))
        return claims
