from bs4 import BeautifulSoup
from collections import namedtuple
import requests
import urllib.parse


ExtractedLink = namedtuple('ExtractedLink', 'url url_quoted text')

ExtractedContent = namedtuple(
    'ExtractedContent',
    'title text image_urls links')


def div_class_paragraph_extractor(soup, cls):
    result = []
    for match in soup.find_all(class_=cls):
        paragraphs = match.find_all('p')
        if len(paragraphs) > 0:
            for paragraph in paragraphs:
                result.append(paragraph.get_text())
        else:
            result.append(match.get_text())
    return result


def link_extractor(soup):
    # Only report links that have more than 4 words in the title
    return [ExtractedLink(
                link.get('href'),
                urllib.parse.quote_plus(link.get('href')),
                link.get_text())
            for link in soup.find_all('a')
            if len(link.get_text().split()) > 4]


def extract_content_from_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.text, 'html.parser')
    extracted_paragraphs = div_class_paragraph_extractor(
        soup, ['article--text', 'articleBody', 'art_content'])
    return ExtractedContent(
        title=soup.title.string,
        text=extracted_paragraphs,
        image_urls=[img.get('src') for img in soup.find_all('img')],
        links=link_extractor(soup))
