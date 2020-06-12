class ContentRating:
    def __call__(self, extracted_content):
        """
        :param extracted_content: Extracted content to rate.
        :return: Value between 0 (worst) and 1 (best)
        """
        raise NotImplementedError


class DummyContentRating(ContentRating):
    def __call__(self, extracted_content):
        return 1
