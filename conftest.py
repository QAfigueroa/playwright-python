import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.fixture
def home_page(page: Page) -> HomePage:
    """Proporciona el objeto de página principal para cada prueba."""
    return HomePage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Proporciona el objeto de la pantalla de login y registro."""
    return LoginPage(page)
