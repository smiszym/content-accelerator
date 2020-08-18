from bs4 import BeautifulSoup

from contentacc.content import ExtractedContent
from contentacc.extractors import ContentExtractor
from contentacc.semantics.guessing import main_content_classes


def html_element_paragraph_extractor(html_element):
    paragraphs = html_element.find_all([
        'p', 'section', 'h1', 'h2', 'h3', 'h4'])
    if len(paragraphs) > 0:
        for paragraph in paragraphs:
            yield paragraph.get_text()
    else:
        yield html_element.get_text()


def div_class_paragraph_extractor(soup, cls):
    for match in soup.find_all(class_=cls):
        for paragraph in html_element_paragraph_extractor(match):
            yield paragraph


def div_id_paragraph_extractor(soup, id):
    for match in soup.find_all(id=id):
        for paragraph in html_element_paragraph_extractor(match):
            yield paragraph


class DivParagraphContentExtractor(ContentExtractor):
    def __call__(self, _, response_text):
        soup = BeautifulSoup(response_text, 'html.parser')
        classes = main_content_classes(soup)
        extracted_paragraphs = (
            list(div_class_paragraph_extractor(soup, classes))
            + list(div_id_paragraph_extractor(soup, classes)))
        return ExtractedContent(
            title=soup.title.string,
            text='\n'.join(f"<p>{par}</p>" for par in extracted_paragraphs))
