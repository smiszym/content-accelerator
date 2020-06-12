from urllib.parse import ParseResult, urlparse, urlunparse


def supply_scheme_and_netloc(url, document_url):
    # TODO: Support relative paths in URLs
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return url  # url parameter is a full URL
    document_parsed_url = urlparse(document_url)
    return urlunparse(ParseResult(
        scheme=document_parsed_url.scheme,
        netloc=document_parsed_url.netloc,
        path=parsed_url.path,
        params='',
        query='',
        fragment=''))
