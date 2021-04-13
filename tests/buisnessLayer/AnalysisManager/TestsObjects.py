from dataclasses import dataclass


@dataclass
class Name:
    name: str

@dataclass
class Status:
    id: str
    author: Name
    content: str

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
    emotion: str
    sentiment: int
    is_fake: str

@dataclass
class Claim:
    name: str
    tweets: list