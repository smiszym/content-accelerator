import bleach
from bs4 import BeautifulSoup
from collections import namedtuple

from contentacc.bs_utils import rewrite_link_targets
from contentacc.extractors.link import link_extractor
from contentacc.extractors.paragraph import \
    div_class_paragraph_extractor, div_id_paragraph_extractor
from contentacc.url_utils import supply_scheme_and_netloc
import json


class ExtractedContent (namedtuple('ExtractedContent',
                                   'title text image_urls links')):
    def to_json(self):
        return json.dumps({
            "title": self.title,
            "text": self.text,
            "image_urls": self.image_urls,
            "links": [link.as_dict() for link in self.links]})


class ContentExtractor:
    def __call__(self, url, response_text):
        raise NotImplementedError


class DivParagraphContentExtractor(ContentExtractor):
    def __call__(self, _, response_text):
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
            text='\n'.join(f"<p>{par}</p>" for par in extracted_paragraphs),
            image_urls=[img.get('src') for img in soup.find_all('img')],
            links=list(link_extractor(soup)))


class MediaWikiContentExtractor(ContentExtractor):
    def __call__(self, url, response_text):
        soup = BeautifulSoup(response_text, 'html.parser')
        article_root = soup.find(class_='mw-parser-output')
        rewrite_link_targets(soup, lambda x: supply_scheme_and_netloc(x, url))
        text = article_root.decode_contents()
        cleaned_text = bleach.clean(
            text,
            strip=True,
            tags=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'p', 'a', 'ul', 'ol',
                  'nl', 'li', 'b', 'i', 'strong', 'em', 'strike', 'abbr', 'code', 'hr', 'br', 'div',
                  'table', 'thead', 'caption', 'tbody', 'tr', 'th', 'td', 'pre', 'iframe'])
        return ExtractedContent(
            title=soup.title.string,
            text=cleaned_text,
            image_urls=[img.get('src') for img in soup.find_all('img')],
            links=[])
