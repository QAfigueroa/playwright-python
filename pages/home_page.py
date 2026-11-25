from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    """Acciones y elementos de la página principal."""

    URL = "https://automationexercise.com/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def abrir(self) -> None:
        """Navega a la página principal."""
        self.ir_a(self.URL)
