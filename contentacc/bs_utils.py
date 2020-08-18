def rewrite_link_targets(soup, f):
    for link in soup.find_all('a'):
        try:
            link['href'] = f(link['href'])
        except KeyError:
            pass
    return soup


def html_classes(soup):
    classes = set()
    for element in soup.find_all(True):
        element_classes = element.get('class')
        if element_classes is not None:
            classes.update(element_classes)
    return classes


def sort_in_html_order(tags, soup):
    def position_in_soup(soup):
        all_elements = soup.find_all()
        return lambda element: all_elements.index(element)
    return sorted(tags, key=position_in_soup(soup))
