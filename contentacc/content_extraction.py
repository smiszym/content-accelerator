from bs4 import BeautifulSoup
from collections import namedtuple
from contentacc.extractors.link import link_extractor
from contentacc.extractors.paragraph import \
    div_class_paragraph_extractor, div_id_paragraph_extractor
import requests


ExtractedContent = namedtuple(
    'ExtractedContent',
    'title text image_urls links')


def extract_content_from_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.text, 'html.parser')
    extracted_paragraphs = div_class_paragraph_extractor(
        soup, ['article--text', 'articleBody', 'art_content',
               'article-story-content', 'article-body',
               'article_body'])
    extracted_paragraphs += div_id_paragraph_extractor(
        soup, ['article--text', 'articleBody', 'art_content',
               'article-story-content', 'article-body',
               'article_body'])
    return ExtractedContent(
        title=soup.title.string,
        text=extracted_paragraphs,
        image_urls=[img.get('src') for img in soup.find_all('img')],
        links=link_extractor(soup))
