def div_class_paragraph_extractor(soup, cls):
    for match in soup.find_all(class_=cls):
        paragraphs = match.find_all('p')
        if len(paragraphs) > 0:
            for paragraph in paragraphs:
                yield paragraph.get_text()
        else:
            yield match.get_text()


def div_id_paragraph_extractor(soup, id):
    for match in soup.find_all(id=id):
        paragraphs = match.find_all('p')
        if len(paragraphs) > 0:
            for paragraph in paragraphs:
                yield paragraph.get_text()
        else:
            yield match.get_text()
