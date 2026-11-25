from playwright.sync_api import Locator, Page


class BasePage:
    """Operaciones comunes que pueden reutilizar las páginas del sitio."""

    def __init__(self, page: Page) -> None:
        # La página del navegador se comparte con cada objeto de página.
        self.page = page

    def ir_a(self, url: str) -> None:
        """Abre una URL y espera a que termine la navegación."""
        self.page.goto(url, wait_until="domcontentloaded")

    def hacer_clic(self, selector: str) -> None:
        """Hace clic en un elemento identificado por su selector."""
        self.page.locator(selector).click()

    def escribir(self, selector: str, texto: str) -> None:
        """Rellena un campo de formulario."""
        self.page.locator(selector).fill(texto)

    def obtener_titulo(self) -> str:
        """Devuelve el título actual de la pestaña."""
        return self.page.title()

    def obtener_elemento(self, selector: str) -> Locator:
        """Devuelve un localizador para permitir comprobaciones más específicas."""
        return self.page.locator(selector)
