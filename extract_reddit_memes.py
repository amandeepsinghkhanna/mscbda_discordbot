"""
	@script-author: Amandeep Singh Khanna
	@script-description: This is a python module that will extract/scrape memes 
	from the specified subreddits using the reddit API.
	@python-version: 3.9.5
	@module-version: 2.0 alpha
	@last-build-date: 30-05-2021
"""


# Importing standard python modules:
import json
import time
from datetime import datetime

# Importing external python modules:
import discord
import requests
import pandas as pd
from tqdm import tqdm

# Importing user-defined python modules:


class ExtractMemes(object):
	"""
		@class-name: ExtractMemes
		@class-description: This class will make requests to the reddit API for 
		the specified subreddits and returns a pandas.core.DataFrame object as 
		an output.
		@input-parameters:
		------------------
		1. subreddit_urls: 
		2. required_media:
		3. max_requests:
		4. req_delay:
	"""
	def __init__(self, subreddit_urls, required_media, max_requests, req_delay):
		self.subreddit_urls = subreddit_urls
		self.required_media = required_media
		self.max_requests = max_requests
		self.req_delay = req_delay
		self.required_keys = [
			 "subreddit_name_prefixed",
			 "upvote_ratio",
			 "ups",
			 "downs",
			 "over_18",
			 "is_video",
			 "url",
			 "permalink",
			 "title"
		]


	def make_requests(self, url):
		for request_attempt in range(self.max_requests):
			time.sleep(self.req_delay)
			request_response = requests.get(
				url=url,
				headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                        + "AppleWebKit/537.36 (KHTML, like Gecko) "
                        + "Chrome/39.0.2171.95 Safari/537.36"
                    )
                }
			)
			if request_response.ok:
				break
		if request_response.ok:
			return request_response.json()
		else:
			return None


	def clean_response(self, request_response):
		cleaned_responses = []
		try:
			posts_lst = request_response["data"]["children"]
			if len(posts_lst) > 0:
				for post in posts_lst:
					if isinstance(post, dict):
						if "data" in list(post.keys()):
							post = post["data"]
							if (
								len(
									set(post.keys())
									.intersection(
										set(self.required_keys)
									)
								) == len(self.required_keys)
							):
								temp_post = {}
								for required_key in self.required_keys:
									temp_post[required_key] = post[required_key]
								cleaned_responses.append(temp_post)
								del temp_post
							else:
								continue
						else:
							continue
					else:
						continue
				return cleaned_responses 		
			else:
				return None
		except Exception as incorrect_response_type:
			return None


	def get_responses(self):
		subreddit_responses = []
		for subreddit_url in tqdm(self.subreddit_urls):
			subreddit_response = self.make_requests(url=subreddit_url)
			if isinstance(subreddit_response, dict):
				subreddit_response_cleaned = self.clean_response(
					subreddit_response
				)
				if subreddit_response_cleaned != None:
					subreddit_responses.append(subreddit_response_cleaned)
			else:
				continue
		if len(subreddit_responses) > 0:
			subreddit_responses = [
				inner_lst 
				for outer_lst in subreddit_responses 
				for inner_lst in outer_lst
			]
			subreddit_responses_df = pd.DataFrame(subreddit_responses)
			subreddit_responses_df["media_format"] = (
				subreddit_responses_df["url"].apply(lambda x: x[-4:])
				.str.lower()
			)
			subreddit_responses_df = (
				subreddit_responses_df[
					subreddit_responses_df["media_format"].isin(self.required_media)
				]
			)
			subreddit_responses_df["shared_flag"] = False
			return subreddit_responses_df
		else:
			return None