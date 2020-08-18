from contentacc.bs_utils import html_classes, sort_in_html_order
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


def test_sort_in_html_order_1():
    soup = BeautifulSoup('<html><body><p class="a">a</p><p class="b">b</p><p class="c"></p></body></html>',
                         'html.parser')
    a = soup.find(class_='a')
    b = soup.find(class_='b')
    c = soup.find(class_='c')
    sorted = sort_in_html_order([c, a, b], soup)
    assert sorted[0] is a
    assert sorted[1] is b
    assert sorted[2] is c
