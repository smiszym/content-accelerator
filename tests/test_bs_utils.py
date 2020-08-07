from contentacc.bs_utils import html_classes
from bs4 import BeautifulSoup


def test_html_classes_1():
    soup = BeautifulSoup('<html><body><p>a</p><p class="xyz">b</p></body></html>', 'html.parser')
    assert html_classes(soup) == {'xyz'}


def test_html_classes_2():
    soup = BeautifulSoup('<html><body><p class="123">a</p><p class="ABC">b</p></body></html>', 'html.parser')
    assert html_classes(soup) == {'ABC', '123'}


def test_html_classes_3():
    soup = BeautifulSoup('<html><body><p class="a1 b2 c3">a</p></body></html>', 'html.parser')
    assert html_classes(soup) == {'a1', 'b2', 'c3'}
