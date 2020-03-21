def html_element_paragraph_extractor(html_element):
    paragraphs = html_element.find_all('p')
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
