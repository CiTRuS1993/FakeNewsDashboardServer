from dataclasses import dataclass


@dataclass
class Name:
    name: str
    location:str =""
@dataclass
class Status:
    id: str
    author: Name
    text: str
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
    emotion: str = "sad"
    sentiment: int = 0
    is_fake: str = "True"

@dataclass
class Claim:
    name: str
    tweets: list

@dataclass
class userObject():
    username: str
    password: str
    role: str
    email: str
    #user_searches = relationship('SearchORM', secondary=SearchHistory, backref='users')
