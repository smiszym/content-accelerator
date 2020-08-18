from bs4 import BeautifulSoup

from contentacc.content import ExtractedContent
from contentacc.extractors import ContentExtractor
from contentacc.semantics.guessing import main_content_classes


def html_element_paragraph_extractor(html_element):
    paragraphs = html_element.find_all([
        'p', 'section', 'h1', 'h2', 'h3', 'h4'])
    if len(paragraphs) > 0:
        for paragraph in paragraphs:
            # Ignore HTML elements that have sub-elements
            if len(paragraph) == 1:
                yield paragraph
    else:
        # Ignore HTML elements that have sub-elements
        if len(html_element) == 1:
            yield html_element


def div_class_paragraph_extractor(soup, cls):
    for match in soup.find_all(class_=cls):
        for paragraph in html_element_paragraph_extractor(match):
            yield paragraph


def div_id_paragraph_extractor(soup, id):
    for match in soup.find_all(id=id):
        for paragraph in html_element_paragraph_extractor(match):
            yield paragraph


def delete_duplicates(seq):
    seen = set()
    pos = 0
    for item in seq:
        if item not in seen:
            seen.add(item)
            seq[pos] = item
            pos += 1
    del seq[pos:]


class DivParagraphContentExtractor(ContentExtractor):
    def __call__(self, _, response_text):
        soup = BeautifulSoup(response_text, 'html.parser')
        classes = main_content_classes(soup)
        extracted_paragraphs = (
            list(div_class_paragraph_extractor(soup, classes))
            + list(div_id_paragraph_extractor(soup, classes)))
        delete_duplicates(extracted_paragraphs)
        final_text = '\n'.join(
            f"<p>{par.get_text(strip=True)}</p>"
            for par in extracted_paragraphs)
        return ExtractedContent(
            title=soup.title.string,
            text=final_text)
