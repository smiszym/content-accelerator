def looks_like_main_content_class(class_name):
    return any(substring in class_name for substring in [
                   'article--text', 'articleBody', 'art_content',
                   'article-story-content', 'article-body',
                   'article_body', 'bodyContent', 'article_wrapper'])


def looks_like_title_class(class_name):
    return any(substring in class_name for substring in ['title'])


def looks_like_lead_class(class_name):
    return any(substring in class_name for substring in ['lead'])


def looks_like_section_header_class(class_name):
    return any(substring in class_name for substring in ['sub_title'])


def looks_like_paragraph_class(class_name):
    return any(substring in class_name for substring in ['paragraph'])


def content_classes(classes):
    return [name for name in classes
            if any(predicate(name) for predicate in [
                looks_like_main_content_class,
                looks_like_title_class,
                looks_like_lead_class,
                looks_like_section_header_class,
                looks_like_paragraph_class])]
