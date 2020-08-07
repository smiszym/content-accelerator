def looks_like_main_content_class(class_name):
    return any(substring in class_name for substring in [
                   'article--text', 'articleBody', 'art_content',
                   'article-story-content', 'article-body',
                   'article_body', 'bodyContent', 'article_wrapper'])


def looks_like_title_class(class_name):
    return any(substring in class_name for substring in ['article_title'])


def looks_like_lead_class(class_name):
    return any(substring in class_name for substring in ['article_lead'])


def looks_like_section_header_class(class_name):
    return any(substring in class_name for substring in ['art_sub_title'])


def looks_like_paragraph_class(class_name):
    return any(substring in class_name for substring in ['art_paragraph'])


def main_content_classes(classes):
    return [name for name in classes if looks_like_main_content_class(name)]


def title_classes(classes):
    return [name for name in classes if looks_like_title_class(name)]


def lead_classes(classes):
    return [name for name in classes if looks_like_lead_class(name)]


def section_header_classes(classes):
    return [name for name in classes if looks_like_section_header_class(name)]


def paragraph_classes(classes):
    return [name for name in classes if looks_like_paragraph_class(name)]
