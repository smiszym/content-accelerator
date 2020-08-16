from collections import namedtuple


class ExtractedContent(namedtuple('ExtractedContent', 'title text')):
    pass


class ContentMetadata(namedtuple('ContentMetadata', 'cache_used fetch_time')):
    """
    Metadata about extracted content.

    cache_used -- True (cached value was returned) or False (the content
                  was fetched from the Internet just now)
    fetch_time -- date and time when the content was fetched from the Internet
    """
    pass
