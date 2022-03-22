# Importing standard python modules:
import os
import json
import sqlalchemy
import pandas as pd

# Importing user-defined python modules:
from reddit_meme_extractor import GetRedditMemes

# Defining global variables:
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

# Python boiler-plate:
if __name__ == "__main__":
    # TODO: Add the code to check if the '.db' file already exists in the directory.
    reddit_retriver = GetRedditMemes(subreddit_urls=SUBREDDIT_URLS)
    reddit_meme_links = reddit_retriver.get_meme_links()