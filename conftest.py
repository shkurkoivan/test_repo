import pytest


def pytest_addoption(parser):
    parser.addoption('--login', action='store', default=None,
                     help="Save users credentials")
    parser.addoption('--password', action='store', default=None,
                     help="Save users credentials")


@pytest.fixture(scope="function")
def basic_auth(request):
    #login_info = request.config.getoption("login")
    #password_info = request.config.getoption("password")
    #credentials = (login_info, password_info)
    credentials =('vanya.shcurko@gmail.com', 'APZrVp83vFNk5F')
    yield credentials
