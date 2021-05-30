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


	def clean_response(self):
		pass


	def get_responses(self):
		pass
