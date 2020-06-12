from contentacc.extractors.content import DivParagraphContentExtractor, \
    ExtractedContent
from contentacc.rating.rating import DummyContentRating
import logging
import redis
import requests
from functools import wraps
import statistics
from typing import Optional


logging.basicConfig(level=logging.INFO)


html_cache = redis.Redis(
    host='localhost', port=6379, db=0, decode_responses=True)


def cache_response(f):
    @wraps(f)
    def wrapper(url, cache_only=False):
        response = html_cache.get(url)
        if response is not None:
            logging.info("Retrieved HTTP response from cache")
            return response
        else:
            if not cache_only:
                logging.info("HTTP response not found in cache, downloading")
                r = f(url)
                html_cache.set(url, r)
                return r
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
    _ = url  # url is needed because this function is wrapped in cache_content
    extractors = [DivParagraphContentExtractor()]
    rating_providers = [DummyContentRating()]
    extracted_content = []
    for extractor in extractors:
        content = extractor(response_text)
        rating = statistics.mean(rating(content) for rating in rating_providers)
        extracted_content.append((content, rating))
    best_content, _ = max(extracted_content, key=lambda x: x[1])
    return best_content


def extract_content_from_url(url: str) -> ExtractedContent:
    response_text = get_response(url)
    extracted_content = extract_content_from_html(url, response_text, bypass_cache=True)
    return extracted_content
