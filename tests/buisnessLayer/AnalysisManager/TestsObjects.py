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