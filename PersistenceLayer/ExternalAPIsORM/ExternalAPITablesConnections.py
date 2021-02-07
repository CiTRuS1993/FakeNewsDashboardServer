from sqlalchemy import Table, Column, ForeignKey, Integer, String
from ..database import Base

TrendsTweetsConnection = Table('TrendsTweetsConnection',
                               Base.metadata,
                               Column('tweet', String, ForeignKey('tweets.id')),
                               Column('trend', Integer, ForeignKey('trends.id')))

SearchTweetConnection = Table('SearchTweetConnection',
                              Base.metadata,
                              Column('tweet', String, ForeignKey('tweets.id')),
                              Column('search', Integer, ForeignKey('search.search_id')))


SnopesTweetsConnection = Table('SnopesTweetsConnection',
                               Base.metadata,
                               Column('tweet', String, ForeignKey('tweets.id')),
                               Column('snope', Integer, ForeignKey('snopes.claim_id')))
