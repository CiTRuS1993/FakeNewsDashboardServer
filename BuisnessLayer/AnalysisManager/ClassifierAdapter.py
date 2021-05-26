import subprocess
import time
from random import random, randint, randrange

from bertopic import BERTopic
import numpy as np
from BuisnessLayer.AnalysisManager.DataObjects import AnalyzedTweet, Claim
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import text2emotion as te


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


author_columns = ['name', 'domain', 'author_guid', 'author_screen_name',
                  'author_full_name', 'author_osn_id', 'description', 'created_at',
                  'statuses_count', 'followers_count', 'favourites_count',
                  'friends_count', 'listed_count', 'language', 'profile_background_color',
                  'profile_background_tile', 'profile_banner_url', 'profile_image_url',
                  'profile_link_color', 'profile_sidebar_fill_color',
                  'profile_text_color', 'default_profile', 'contributors_enabled',
                  'default_profile_image', 'geo_enabled', 'protected', 'location',
                  'notifications', 'time_zone', 'url', 'utc_offset', 'verified',
                  'is_suspended_or_not_exists', 'default_post_format', 'likes_count',
                  'allow_questions', 'allow_anonymous_questions', 'image_size',
                  'media_path', 'author_type', 'bad_actors_collector_insertion_date',
                  'xml_importer_insertion_date', 'vico_dump_insertion_date',
                  'missing_data_complementor_insertion_date',
                  'bad_actors_markup_insertion_date',
                  'mark_missing_bad_actor_retweeters_insertion_date', 'author_sub_type',
                  'timeline_overlap_insertion_date',
                  'original_tweet_importer_insertion_date']

post_columns = ['post_id', 'author', 'guid', 'title', 'url', 'date', 'content',
                'description', 'is_detailed', 'is_LB', 'is_valid', 'domain',
                'author_guid', 'media_path', 'post_osn_guid', 'post_type',
                'post_format', 'reblog_key', 'tags', 'is_created_via_bookmarklet',
                'is_created_via_mobile', 'source_url', 'source_title', 'is_liked',
                'post_state', 'post_osn_id', 'retweet_count', 'favorite_count',
                'created_at', 'xml_importer_insertion_date',
                'timeline_importer_insertion_date',
                'original_tweet_importer_insertion_date']

claims_columns = ['claim_id', 'title', 'description', 'url', 'verdict_date', 'keywords',
                  'domain', 'verdict', 'category', 'sub_category']

connection_columns = ['claim_id', 'post_id']

# subprocess.call(['python','run_dataset_builder.py','configuration/config_demo.ini'],cwd= r'D:\aviad fake v3\fake-news-framework_Py3',shell=True)
# ours, should write also stub
class ClassifierAdapter:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    def get_sentiment(self,text) -> int:
        snt = self.sid.polarity_scores(text)
        return snt['pos']*3-snt['neg']*3

    def get_emotion(self,text):
        return max(te.get_emotion(text))  # The output we received,

    def _trends_to_csv(self, trends_dict, path="D:/aviad fake v3/fake-news-framework_Py3/data/input/D/"):
        topics = []
        tweets = []
        authors = []
        topic_tweet_connection = []

        for trend in trends_dict.keys():
            for topic in trends_dict[trend].claims:
                topics.append({'title': topic.name})  # check what is the input
                for tweet in topic.tweets:
                    topic_tweet_connection.append({'topic_id': topic.id, 'tweet_id': tweet.id})
                    tweets.append(tweet.__dict__)
                    authors.append(tweet.author)

        pd.DataFrame(topics, columns=claims_columns).to_csv(path + "claims.csv",index=False)
        pd.DataFrame(tweets, columns=post_columns).to_csv(path + "posts.csv",index=False)
        pd.DataFrame(authors, columns=author_columns).to_csv(path + "authors.csv",index=False)
        pd.DataFrame(topic_tweet_connection, columns=connection_columns).to_csv(path + "claim_tweet_connection.csv",index=False)

    def _classify_op(self):
        subprocess.call(['python','run_dataset_builder.py','configuration/config_demo.ini'],cwd= r'D:\aviad fake v3\fake-news-framework_Py3',shell=True)
        results = pd.read_csv("D:\\aviad fake v3\\fake-news-framework_Py3\\data\\output\\D")[['ClaimFeatureGenerator_claim_id','pred']]
        return results


    def analyze_trends(self, trends_dict, callback):  # trends_dict is type of dict {<trend name> : <Trend>}
        processed_data = {}
        self._trends_to_csv(trends_dict)
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
                processed_data[trend].append(Claim(topic.name, tweets))

        time.sleep(1)
        return callback(processed_data, trends_dict)

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
                claims["claim1"][status.id]= {'id': status.id, 'author': status.author.name, 'content': status.text}
            else:
                claims["claim2"][status.id]= {'id': status.id, 'author': status.author.name, 'content': status.text}
        return claims

    def _get_claim_from_trend(self, trends_tweets):
        df = pd.DataFrame([tweet.__dict__ for tweet in trends_tweets])[['id', 'text']]
        if len(df) < 15:
            from collections import Counter
            claim_text = ' '.join([txt[0] for txt in
                                   Counter(" ".join(df['text'].str.replace("RT", '').values).split(' ')).most_common(
                                       10)])
            return [Claim(claim_text, df['id'].values)]
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
