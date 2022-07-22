from datetime import date, datetime
from typing import List

import pytest

from wsgi import  Blog



@pytest.fixture()
def blog():
    return Blog('title0', 'content0')

def test_blog(blog):
    assert blog.title == 'title0'

def test_blog_II(blog):
    assert blog.text == 'content0'