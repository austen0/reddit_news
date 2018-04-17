# reddit_news

A Reddit bot to automatically submit news articles sourced from [NewsAPI.org](https://newsapi.org/) to a given subreddit.

## Prerequisites

* [Reddit OAuth2 Credentials](https://github.com/reddit-archive/reddit/wiki/OAuth2)
* [NewsAPI.org API Key](https://newsapi.org/register)

## Set-up Guide

1. Install PyPI dependencies.
   ```bash
   pip install logzero newsapi-python praw unidecode
   ```
1. Clone git project to local directory.
   ```bash
   git clone https://github.com/austen0/reddit_news.git
   ```
1. Create `config.py` in `reddit_news/` and configure per the following template.
   ```python
   REDDIT_CLIENT_ID = 'XXX'
   REDDIT_CLIENT_SECRET = 'XXX'
   REDDIT_USERNAME = 'XXXX'
   REDDIT_PASSWORD = 'XXXX'

   NEWSAPI_KEY = 'XXX'

   RUN_FREQUENCY_MINS = 30

   LANGUAGE = 'en'

   # List of valid news sources: https://newsapi.org/sources
   FEEDS = {
     'subreddit_name1': 'news-source1',
     'subreddit_name2': 'news-source1',
   }
   ```

1. Execute the script and it will continue to run indefinitely.
   ```bash
   ./reddit_news.py
   ```
