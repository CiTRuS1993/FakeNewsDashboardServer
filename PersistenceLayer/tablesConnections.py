from sqlalchemy import Table, Column, ForeignKey, Integer, String
from .database import Base

TagsUsersConnection = Table('TagsUsersConnection',
                               Base.metadata,
                               Column('tweet', String, ForeignKey('tweets.id'), primary_key=True),
                               Column('user', Integer, ForeignKey('users.username'), primary_key=True),
                               Column('tag', String)
                               )

SearchHistory = Table('SearchHistory',
                      Base.metadata,
                      Column('search', Integer, ForeignKey('search.search_id'), primary_key=True),
                      Column('users', Integer, ForeignKey('users.username'), primary_key=True)
                      )
TopicsTrendsConnection = Table('TopicsTrendsConnection',
                               Base.metadata,
                               Column('topic', Integer, ForeignKey('analysed_topics.id'), primary_key=True),
                               Column('trend', Integer, ForeignKey('trends.id'), primary_key=True)
                               )

TopicsTweetsConnection = Table('TopicsTweetsConnection',
                               Base.metadata,
                               Column('topic', Integer, ForeignKey('analysed_topics.id'), primary_key=True),
                               Column('tweet', String, ForeignKey('tweets.id'), primary_key=True)
                               )
