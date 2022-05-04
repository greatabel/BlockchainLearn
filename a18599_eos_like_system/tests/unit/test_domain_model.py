from datetime import date

from wsgi import  User

import pytest


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')

def test_user(user):
    assert user.username == 'dbowie'


