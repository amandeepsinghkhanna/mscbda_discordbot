# Importing standard python modules:
import time
from datetime import datetime


# Importing external python modules:
import requests
import pandas as pd
from tqdm import tqdm


# User-defined class to Extract memes from reddit:
class GetRedditMemes(object):
    """
    GetRedditMemes: Connects to the specified subreddits & extracts memes
    from them.
    """

    # Class Variables:
    MAX_REQUESTS = 10
    REQUEST_DELAY = 1
    REQUEST_HEADER = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
            + "AppleWebKit/537.36 (KHTML, like Gecko) "
            + "Chrome/39.0.2171.95 Safari/537.36"
        )
    }
    REQUIRED_METADATA = [
        "subreddit_name_prefixed",
        "upvote_ratio",
        "ups",
        "downs",
        "over_18",
        "is_video",
        "url",
        "permalink",
        "title",
    ]
    REQUIRED_FORMATS = [".jpg", "jpeg", ".png"]

    def __init__(self, subreddit_urls):
        self.subreddit_urls = subreddit_urls

    def make_requests(self, url):
        for request_attempt in range(self.MAX_REQUESTS):
            time.sleep(self.REQUEST_DELAY)
            request_response = requests.get(url=url, headers=self.REQUEST_HEADER)
            if request_response.ok:
                break
        if request_response.ok:
            return request_response.json()
        else:  # If all requests to the subreddits have failed!
            return None

    def clean_reddit_response(self, request_response):
        cleaned_posts = []
        post_list = request_response.get("data").get("children")
        if isinstance(post_list, list):
            if len(post_list) >= 1:
                for post in post_list:
                    if isinstance(post, dict):
                        if post.get("data") != None:
                            post = post.get("data")
                            metadata_fields_missing_check = [
                                metadata_field
                                for metadata_field in self.REQUIRED_METADATA
                                if metadata_field not in post.keys()
                            ]
                            if len(metadata_fields_missing_check) == 0:
                                post = {
                                    key: value
                                    for key, value in post.items()
                                    if key in self.REQUIRED_METADATA
                                }
                                cleaned_posts.append(post)
        if len(cleaned_posts) >= 1:
            return cleaned_posts
        else:
            return None

    def get_redditmeme_links(self):
        meme_links = []
        for subreddit_url in tqdm(self.subreddit_urls):
            subreddit_response = self.make_requests(url=subreddit_url)
            if subreddit_response != None:
                subreddit_response_cleaned = self.clean_reddit_response(
                    subreddit_response
                )
                if subreddit_response_cleaned != None:
                    meme_links.extend(subreddit_response_cleaned)
        if len(meme_links) >= 1:
            meme_links = pd.DataFrame(meme_links)
            meme_links["media_format"] = (
                meme_links["url"].apply(lambda x: x[-4:]).str.lower()
            )
            meme_links = meme_links.loc[
                meme_links["media_format"].isin(self.REQUIRED_FORMATS)
            ]
            meme_links["post_id"] = meme_links["url"].apply(
                lambda x: x.split("/")[-1][:-4]
            )
            meme_links["extraction_timestamp"] = datetime.now().strftime(
                format="%d%m%d"
            )
            meme_links["link_source"] = "REDDIT"
            meme_links = meme_links.drop_duplicates(subset=["post_id"])
            if meme_links.shape[0] >= 1:
                return meme_links
        else:
            return None