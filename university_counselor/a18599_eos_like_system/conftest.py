import os
import pytest

from movie import create_app



TEST_DATA_PATH = os.path.join("movie", "tests", "data")
# TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'iwar006', 'Documents', 'Python dev', 'COVID-19', 'tests', 'data')





@pytest.fixture
def client():
    my_app = create_app(
        {
            "TESTING": True,  # Set to True during testing.
            "TEST_DATA_PATH": TEST_DATA_PATH,  # Path for loading test data into the repository.
            "WTF_CSRF_ENABLED": False,  # test_client will not send a CSRF token, so disable validation.
        }
    )

    return my_app.test_client()
