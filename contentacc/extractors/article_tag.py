from bs4 import BeautifulSoup

from contentacc.content import ExtractedContent
from contentacc.extractors import ContentExtractor
from contentacc.extractors.div_paragraph import \
    html_element_paragraph_extractor


class ArticleTagContentExtractor(ContentExtractor):
    def __call__(self, _, response_text):
        soup = BeautifulSoup(response_text, 'html.parser')
        article_tags = soup.find_all('article')
        if len(article_tags) != 1:
            # 0 - nothing found; more than 1 - which one to choose?
            return
        final_text = '\n'.join(
            f"<p>{par.get_text(strip=True)}</p>"
            for par in html_element_paragraph_extractor(article_tags[0]))
        return ExtractedContent(
            title=soup.title.string,
            text=final_text)
