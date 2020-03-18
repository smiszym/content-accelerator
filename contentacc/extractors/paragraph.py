def div_class_paragraph_extractor(soup, cls):
    result = []
    for match in soup.find_all(class_=cls):
        paragraphs = match.find_all('p')
        if len(paragraphs) > 0:
            for paragraph in paragraphs:
                result.append(paragraph.get_text())
        else:
            result.append(match.get_text())
    return result


def div_id_paragraph_extractor(soup, id):
    result = []
    for match in soup.find_all(id=id):
        paragraphs = match.find_all('p')
        if len(paragraphs) > 0:
            for paragraph in paragraphs:
                result.append(paragraph.get_text())
        else:
            result.append(match.get_text())
    return result
