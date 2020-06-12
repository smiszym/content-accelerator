from unittest import TestCase

from contentacc.url_utils import supply_scheme_and_netloc


class TestSupplySchemeAndNetloc(TestCase):
    def test_supply_scheme_and_netloc(self):
        assert (supply_scheme_and_netloc(
            '/wiki/Polska',
            'https://pl.wikipedia.org/wiki/Jaszczurka_zwinka')
                == 'https://pl.wikipedia.org/wiki/Polska')
