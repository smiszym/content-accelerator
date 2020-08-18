from bs4 import BeautifulSoup

from contentacc.bs_utils import sort_in_html_order
from contentacc.content import ExtractedContent
from contentacc.extractors import ContentExtractor
from contentacc.semantics.guessing import main_content_classes


def html_element_paragraph_extractor(html_element):
    content_tags = ['p', 'section', 'h1', 'h2', 'h3', 'h4']
    paragraphs = html_element.find_all(content_tags)
    if len(paragraphs) > 0:
        for paragraph in paragraphs:
            # Ignore HTML elements that have sub-elements
            if len(paragraph) == 1:
                yield paragraph
    else:
        # Ignore HTML elements that have sub-elements
        if (len(html_element) == 1
                and html_element.name in content_tags + ['div']):
            yield html_element


def div_class_paragraph_extractor(soup, cls):
    for match in soup.find_all(class_=cls):
        for paragraph in html_element_paragraph_extractor(match):
            yield paragraph


def div_id_paragraph_extractor(soup, id):
    for match in soup.find_all(id=id):
        for paragraph in html_element_paragraph_extractor(match):
            yield paragraph


def all_classes_in_soup(soup):
    result = set()
    for element in soup.find_all():
        try:
            result.update(element['class'])
        except KeyError:
            pass
    return result


class DivParagraphContentExtractor(ContentExtractor):
    def __call__(self, _, response_text):
        soup = BeautifulSoup(response_text, 'html.parser')
        classes = main_content_classes(all_classes_in_soup(soup))
        extracted_paragraphs = sort_in_html_order(
            set(div_class_paragraph_extractor(soup, classes))
            | set(div_id_paragraph_extractor(soup, classes)), soup)
        final_text = '\n'.join(
            f"<p>{par.get_text(strip=True)}</p>"
            for par in extracted_paragraphs)
        return ExtractedContent(
            title=soup.title.string,
            text=final_text)
