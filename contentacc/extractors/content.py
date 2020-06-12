from bs4 import BeautifulSoup
from collections import namedtuple
from contentacc.extractors.link import link_extractor
from contentacc.extractors.paragraph import \
    div_class_paragraph_extractor, div_id_paragraph_extractor
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
    def __call__(self, response_text):
        raise NotImplementedError


class DivParagraphContentExtractor(ContentExtractor):
    def __call__(self, response_text):
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
