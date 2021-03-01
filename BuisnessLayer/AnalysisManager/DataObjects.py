from dataclasses import dataclass


@dataclass
class Trend:
    id: int
    keywords: str
    claims: list


@dataclass
class Claim:
    name: str
    tweets: list


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

# @dataclass
# class AnalyzedTopic(Claim):
#     emotion: str
#     sentiment: int
#     is_fake: str