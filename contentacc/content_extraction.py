from contentacc.extractors.content import DivParagraphContentExtractor, \
    MediaWikiContentExtractor
from contentacc.content import ExtractedContent, ContentMetadata
from contentacc.rating.rating import DummyContentRating
import logging
import redis
import requests
from functools import wraps
import statistics
from typing import Optional


def _setup_redis(redis):
    redis.config_set('maxmemory-policy', 'allkeys-lru')
    config = html_cache.config_get('maxmemory*')
    if config['maxmemory'] == '0':
        logging.error('Redis memory is unlimited. This is discouraged, you will experience performance issues')
    if config['maxmemory-policy'] != 'allkeys-lru':
        logging.error('Redis maxmemory-policy is expected to be "allkeys-lru"')


html_cache = redis.Redis(
    host='localhost', port=6379, db=0, decode_responses=True)


_setup_redis(html_cache)


def cache_response(f):
    @wraps(f)
    def wrapper(url, cache_only=False):
        response = html_cache.get(url)
        if response is not None:
            logging.info("Retrieved HTTP response from cache")
            return response, ContentMetadata(cache_used=True, fetch_time=None)
        else:
            if not cache_only:
                logging.info("HTTP response not found in cache, downloading")
                r = f(url)
                html_cache.set(url, r)
                return r, ContentMetadata(cache_used=False, fetch_time=None)
    return wrapper


def cache_content(f):
    contents = {}
    @wraps(f)
    def wrapper(url, response_text, bypass_cache=False):
        if bypass_cache or not contents.get(url):
            c = f(url, response_text)
            contents[url] = c
            logging.info("Extracted content for HTTP response now")
            return c
        logging.info("Retrieving extracted content from cache")
        return contents[url]
    return wrapper


@cache_response
def get_response(url: str) -> Optional[str]:
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.text


@cache_content
def extract_content_from_html(url, response_text) -> ExtractedContent:
    extractors = [MediaWikiContentExtractor(), DivParagraphContentExtractor()]
    rating_providers = [DummyContentRating()]
    extracted_content = []
    for extractor in extractors:
        content = extractor(url, response_text)
        if content is None:
            continue
        rating = statistics.mean(rating(content) for rating in rating_providers)
        extracted_content.append((content, rating))
    if len(extracted_content) == 0:
        return
    best_content, _ = max(extracted_content, key=lambda x: x[1])
    return best_content


def extract_content_from_url(url: str) -> ExtractedContent:
    response_text, metadata = get_response(url)
    extracted_content = extract_content_from_html(url, response_text)
    return extracted_content, metadata
