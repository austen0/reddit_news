#!/usr/bin/env python

import config
import logging
import logzero
import praw
import time
from newsapi import NewsApiClient
from unidecode import unidecode

LOGGER = logzero.logger


class Reddit(object):

  def __init__(self):
    self.reddit = praw.Reddit(
      client_id=config.REDDIT_CLIENT_ID,
      client_secret=config.REDDIT_CLIENT_SECRET,
      username=config.REDDIT_USERNAME,
      password=config.REDDIT_PASSWORD,
      user_agent='Powered by NewsAPI.org'
    )

  def submit(self, sub, entries):
    LOGGER.info('Submitting latest articles to: %s' % sub)
    subreddit = self.reddit.subreddit(sub)
    for title, url in entries.iteritems():
      try:
        subreddit.submit(
          title,
          url=url,
          resubmit=False,
          send_replies=False
        )
        LOGGER.debug('Article submitted: %s' % title)
      except praw.exceptions.APIException as e:
        LOGGER.debug(e)
      except Exception as e:
        LOGGER.error(e)


class NewsApi(object):

  def __init__(self):
    self.newsapi = NewsApiClient(api_key=config.NEWSAPI_KEY)

  def getTopNews(self, source):
    LOGGER.info('Fetching latest news for: %s' % source)
    top_headlines = dict()
    articles = dict()

    try:
      top_headlines = self.newsapi.get_top_headlines(
        sources=source,
        language=config.LANGUAGE
      )
    except Exception as e:
      LOGGER.error(e)

    if 'articles' in top_headlines:
      for article in top_headlines['articles']:
        title = unidecode(article['title'])
        url = article['url']
        articles[title] = url
    LOGGER.info('Fetch complete. # of articles: %d' % len(articles))
    return articles


def main():
  reddit = Reddit()
  newsapi = NewsApi()
  logzero.logfile(
    'reddit_news.log', maxBytes=1e7, backupCount=3, loglevel=logging.INFO)

  try:
    while True:
      LOGGER.info('Update started.')
      for subreddit, source in config.FEEDS.iteritems():
        articles = newsapi.getTopNews(source)
        reddit.submit(subreddit, articles)

      LOGGER.info('Update complete.')
      time.sleep(config.RUN_FREQUENCY_MINS * 60)
  except KeyboardInterrupt:
    print '\nKeyboard interrupt detected, quitting reddit_news.'


if __name__ == '__main__':
  main()
