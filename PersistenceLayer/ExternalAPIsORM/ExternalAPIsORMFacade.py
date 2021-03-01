from PersistenceLayer.ExternalAPIsORM import AuthorORM, SearchORM, SnopesORM
from PersistenceLayer.ExternalAPIsORM.TrendsORM import TrendsORM
from PersistenceLayer.ExternalAPIsORM.TweetORM import TweetORM


class ExternalAPIsORMFacade:
    def __init__(self):
        from ..database import session
        self.session = session

    def add_trend(self, content, date):
        trend = TrendsORM(content=content, date=date)
        trend.add_to_db()
        return trend.id

    def add_author(self, username, statuses_count=0, followers_count=0, friends_count=0, listed_count=0):
        AuthorORM(username=username, statuses_count=statuses_count, followers_count=followers_count,
                  friends_count=friends_count, listed_count=listed_count).add_to_db()

    def add_tweet_to_author(self, tweet_id, author_username):
        tweet = self.session.query(TweetORM).filter_by(id=tweet_id).first()
        author = self.session.query(AuthorORM).filter_by(username=author_username).first()
        if author is not None:
            author.tweets.append(tweet)
            author.update_db()
        else:
            self.add_author(author_username)
            author = self.session.query(AuthorORM).filter_by(username=author_username).first()
            author.tweets.append(tweet)
            author.update_db()

    def add_tweet(self, id, author_username, content, location, date, trend_id=None, claim_id=None):
        tweet = TweetORM(id=id, author_name=author_username, content=content, date=date, location=location)
        tweet.add_to_db()
        if trend_id is not None:
            trend = self.session.query(TrendsORM).filter_by(id=trend_id).first()
            if trend is not None:
                trend.tweets.append(tweet)
                trend.update_db()
        if claim_id is not None:
            claim = self.session.query(SnopesORM).filter_by(claim_id=claim_id).first()
            if claim is not None:
                claim.snope_tweets.append(tweet)
                claim.update_db()
        self.add_tweet_to_author(id, author_username)

    def add_search(self, keywords):
        search = SearchORM(KeyWords=keywords)
        search.add_to_db()
        return search.search_id

    def add_snopes(self, content, Verdict, Date):
        snope = SnopesORM(content=content, Verdict=Verdict, Date=Date)
        snope.add_to_db()
        return snope.claim_id