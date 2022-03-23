from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer, DateTime, Float


Base = declarative_base()


class MemesDB(Base):
    __tablename__ = 'memes'
    post_id = Column(Text, primary_key=True)
    title = Column(Text)
    subreddit_name_prefixed = Column(Text)
    upvote_ratio = Column(Float)
    ups = Column(Integer)
    url = Column(Text)
    extraction_timestamp = Column(DateTime)
    link_source = Column(Text)