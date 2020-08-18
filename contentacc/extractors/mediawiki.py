import bleach
from bs4 import BeautifulSoup

from contentacc.bs_utils import rewrite_link_targets
from contentacc.content import ExtractedContent
from contentacc.extractors import ContentExtractor
from contentacc.url_utils import supply_scheme_and_netloc
import logging


class MediaWikiContentExtractor(ContentExtractor):
    def __call__(self, url, response_text):
        logging.info("Starting media wiki processing")
        soup = BeautifulSoup(response_text, 'html.parser')
        logging.info("Soup parsed")
        article_root = soup.find(class_='mw-parser-output')
        if article_root is None:
            return
        rewrite_link_targets(soup, lambda x: supply_scheme_and_netloc(x, url))
        logging.info("Links rewritten")
        text = article_root.decode_contents()
        logging.info("Content dumped to text")
        cleaned_text = bleach.clean(
            text,
            strip=True,
            attributes={'a': ['href']},
            tags=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'p', 'a', 'ul', 'ol', 'dl', 'dt', 'dd', 'sup',
                  'nl', 'li', 'b', 'i', 'strong', 'em', 'strike', 'code', 'hr', 'br', 'div',
                  'table', 'thead', 'caption', 'tbody', 'tr', 'th', 'td', 'pre', 'iframe'])
        logging.info("Content cleaned")
        result = ExtractedContent(
            title=soup.title.string,
            text=cleaned_text)
        logging.info("Finished media wiki processing")
        return result
