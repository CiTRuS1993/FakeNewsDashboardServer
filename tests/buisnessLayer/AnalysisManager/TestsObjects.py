from dataclasses import dataclass


@dataclass
class Name:
    name: str

@dataclass
class Status:
    id: str
    author: Name
    text: str

@dataclass
class Trend:
    id: int
    keywords: str

@dataclass
class AnalysedTweet(Status):
    emotion: str
    sentiment: int
    is_fake: str

@dataclass
class userObject():
    username: str
    password: str
    role: str
    email: str
    #user_searches = relationship('SearchORM', secondary=SearchHistory, backref='users')
