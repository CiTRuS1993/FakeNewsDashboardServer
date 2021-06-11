import datetime
from dataclasses import dataclass, field


@dataclass
class Statistics:
    emotion: str
    sentiment: int
    avg_fake: int
    # authenticity: int
    amount: int

    def add_statistics(self, emotions, sentiment, fake):
        amount = len(emotions)
        if amount > 0:
            self.sentiment = sentiment/amount
            self.emotion = self.calc_emotions(emotions)
            self.avg_fake = self.calc_avg_prediction(fake)
            self.amount = self.amount + amount

    def calc_avg_prediction(self, prediction):
        fake_amount = self.avg_fake * self.amount
        return round((prediction['true'] + fake_amount > prediction['fake'] + (self.amount - fake_amount)) / self.amount)


    def calc_emotions(self, emotions):
        emotions_counter = {"Anger":0, "Disgust":0, "Sad":0, "Happy":0, "Surprise": 0, "Fear": 0}
        for emotion in emotions:
            emotions_counter[emotion] = emotions_counter[emotion]+1
        max_emotion_counter = max([emotions_counter[emotion] for emotion in emotions_counter])
        max_emotion = [emotion for emotion in emotions_counter if emotions_counter[emotion]==max_emotion_counter]
        return max_emotion[0]

    def copy_statistics(self, statistics):
        self.sentiment = round((self.sentiment * self.amount) + (statistics.sentiment * statistics.amount) / (self.amount + statistics.amount))
        self.avg_fake = round((self.avg_fake * self.amount) + (statistics.avg_fake * statistics.amount) / (self.amount + statistics.amount))
        if self.amount < statistics.amount:
            self.emotion = statistics.emotion

@dataclass
class WordCloud:
    text: str
    value: int

@dataclass
class TrendStatistic:
    words: list
    statistics: Statistics

@dataclass
class Trend:
    id: int
    keywords: str
    claims: list

@dataclass
class AnalysedTrend(Trend):
    statistics: TrendStatistic

@dataclass
class Claim:
    name: str
    tweets: list

    def setID(self, topic_id):
        self.id: topic_id

@dataclass
class AnalysedClaim(Claim):
    statistics: Statistics # maybe use the ClaimStatistics instead (like the TrendStatistics)

    def get_all_emotions(self):
        emotions_counter = {"Anger": 0, "Disgust": 0, "Sad": 0, "Happy": 0, "Surprise": 0, "Fear": 0}
        for tweet in self.tweets:
            emotions_counter[tweet.emotion] = emotions_counter[tweet.emotion] + 1
        emotions = list()
        for emotion in emotions_counter.keys():
            emotions.append({'y': emotions_counter[emotion], 'label': emotion})
        return emotions


@dataclass
class Tweet:
    id: int
    author: str
    content: str

@dataclass
class AnalyzedTweet(Tweet):
    emotion: str
    sentiment: int
    is_fake: str

@dataclass
class SentimentByDate:
    sentiment: int
    label: str

@dataclass
class Sentiment:
    topics: list
    trends: list
    claims: list

@dataclass
class Temperature:
    # authenticity: int
    sentiment: int
    is_fake: int

    def __post_init__(self):
        if self.sentiment == 3:
            self.sentiment = 100
        elif self.sentiment == 2:
            self.sentiment = 83
        elif self.sentiment == 1:
            self.sentiment = 69
        elif self.sentiment == 0:
            self.sentiment = 50
        elif self.sentiment == -1:
            self.sentiment = 32
        elif self.sentiment == -2:
            self.sentiment = 18
        else:
            self.sentiment = 0
