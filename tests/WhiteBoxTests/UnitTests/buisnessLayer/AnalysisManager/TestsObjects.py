from dataclasses import dataclass


@dataclass
class Name:
    name: str
    location:str =""

@dataclass
class name:
    name: str
    location: str = ""

@dataclass
class Status:
    id: str
    author: Name
    content: str
    created_at:str = ""
    place:str = ""
    user:Name = Name('')
# @dataclass
# class Status1:
#     id: str
#     author: str
#     text: str

@dataclass
class Trend:
    id: int
    keywords: str

@dataclass
class AnalysedTweet(Status):
    emotion: str = "Sad"
    sentiment: int = 0
    is_fake: str = "true"

@dataclass
class Claim:
    name: str
    tweets: list
    id: int

    def setID(self, new_id):
        self.id = new_id

    def get_all_emotions(self):
        return ['Happy', 'Sad']

@dataclass
class Statistics:
    emotion: str
    sentiment: int
    avg_fake: int
    # authenticity: int
    amount: int

@dataclass
class AnalysedTrend(Trend):
    claims: list
    statistics: Statistics = Statistics('Happy', 3, 1, 10)

@dataclass
class userObject():
    username: str
    password: str
    role: str
    email: str
    #user_searches = relationship('SearchORM', secondary=SearchHistory, backref='users')
