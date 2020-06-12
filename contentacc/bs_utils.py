def rewrite_link_targets(soup, f):
    for link in soup.find_all('a'):
        try:
            link['href'] = f(link['href'])
        except KeyError:
            pass
    return soup
