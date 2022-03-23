# Importing standard python modules:
import os


# Importing external python modules:
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


# Importing user-defined python modules:
from reddit_meme_extractor import GetRedditMemes
from db_models import MemesDB


# Defining global variables:

# List of URLs to subreddits to extract memes:
SUBREDDIT_URLS = [
    "https://www.reddit.com/r/wholesomememes/top.json?limit=100&t=3days",
    "https://www.reddit.com/r/funny/top.json?limit=100&t=3days",
    "https://www.reddit.com/r/AdviceAnimals/top.json?limit=100&t=3days",
    "https://www.reddit.com/r/memes/top.json?limit=100&t=3days",
    "https://www.reddit.com/r/ProgrammerHumor/top.json?limit=100&t=3days",
    "https://www.reddit.com/r/MemeEconomy/top.json?limit=100&t=3days",
    "https://www.reddit.com/r/dankmemes/top.json?limit=100&t=3days",
    "https://www.reddit.com/r/terriblefacebookmemes/top.json?limit=100&t=3days",
    "https://www.reddit.com/r/IndianDankMemes/top.json?limit=100&t=3days"
]

class GenerateMemeRepo(GetRedditMemes):

    def __init__(self, subreddit_urls, db_url):
        super().__init__(subreddit_urls)
        self.db_url = db_url
        self.db_engine = create_engine(self.db_url)


    def create_db(self):
        declarative_base().metadata.create_all(self.db_engine)


    def check_db_status(self):
        if os.path.exists(os.path.join(os.getcwd(), self.db_url[9:])) == False:
            self.create_db()

    def ingest_newdata(self):
        self.check_db_status()
        reddit_memes = self.get_redditmeme_links()
        reddit_memes[[
            'post_id',
            'title',
            'subreddit_name_prefixed',
            'upvote_ratio',
            'ups',
            'url',
            'extraction_timestamp',
            'link_source'
        ]].drop_duplicates().to_sql(
            name='memes',
            con=self.db_engine,
            index=False,
            if_exists='append'
        )



