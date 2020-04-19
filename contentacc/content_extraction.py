from bs4 import BeautifulSoup
from collections import namedtuple
from contentacc.extractors.link import link_extractor
from contentacc.extractors.paragraph import \
    div_class_paragraph_extractor, div_id_paragraph_extractor
import requests
from functools import wraps
from typing import Optional
import logging


logging.basicConfig(level=logging.INFO)


ExtractedContent = namedtuple(
    'ExtractedContent',
    'title text image_urls links')


def cache_response(f):
    responses = {}
    @wraps(f)
    def wrapper(url, cache_only=False):
        try:
            response = responses[url]
            logging.info("Retrieved HTTP response from cache")
            return response
        except KeyError:
            if not cache_only:
                r = f(url)
                responses[url] = r
                logging.info("HTTP response not found in cache, downloading")
                return r
    return wrapper


def cache_content(f):
    contents = {}
    @wraps(f)
    def wrapper(url, response_text, bypass_cache=False):
        if bypass_cache or not contents.get(url):
            c = f(url, response_text)
            contents[url] = c
            logging.info("Extracted content now")
            return c
        logging.info("Retrieving extracted content from cache")
        return contents[url]
    return wrapper


@cache_response
def get_response(url: str, **kwargs) -> Optional[str]:
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.text


@cache_content
def extract_content_from_html(url, response_text, **kwargs) -> ExtractedContent:
    soup = BeautifulSoup(response_text, 'html.parser')
    extracted_paragraphs = list(div_class_paragraph_extractor(
        soup, ['article--text', 'articleBody', 'art_content',
               'article-story-content', 'article-body',
               'article_body']))
    extracted_paragraphs += list(div_id_paragraph_extractor(
        soup, ['article--text', 'articleBody', 'art_content',
               'article-story-content', 'article-body',
               'article_body', 'bodyContent']))
    return ExtractedContent(
        title=soup.title.string,
        text=extracted_paragraphs,
        image_urls=[img.get('src') for img in soup.find_all('img')],
        links=list(link_extractor(soup)))


def extract_content_from_url(url: str) -> ExtractedContent:
    response_text = get_response(url)
    extracted_content = extract_content_from_html(url, response_text, bypass_cache=True)
    return extracted_content
