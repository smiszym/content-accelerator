import urllib.parse
from collections import namedtuple


ExtractedLink = namedtuple('ExtractedLink', 'url url_quoted text')


def link_extractor(soup):
    # Only report links that have more than 4 words in the title
    return [ExtractedLink(
                link.get('href'),
                urllib.parse.quote_plus(link.get('href')),
                link.get_text())
            for link in soup.find_all('a')
            if len(link.get_text().split()) > 4
            and link.get('href').startswith('http')]
