from typing import Optional

from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Acciones de inicio de sesión y registro de usuarios."""

    URL = "https://automationexercise.com/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def abrir(self) -> None:
        """Abre la pantalla que contiene los formularios de login y registro."""
        self.ir_a(self.URL)

    def iniciar_sesion(self, email: str, password: str) -> None:
        """Envía las credenciales del formulario de inicio de sesión."""
        self.escribir("#form input[data-qa='login-email']", email)
        self.escribir("#form input[data-qa='login-password']", password)
        self.hacer_clic("#form button[data-qa='login-button']")

    def obtener_error_login(self) -> str:
        """Lee el mensaje que muestra el sitio cuando el login no es válido."""
        return self.obtener_elemento("#form p").filter(
            has_text="Your email or password is incorrect!"
        ).inner_text()

    def registrarse(
        self,
        nombre: str,
        email: str,
        password: str,
        nombre_persona: str,
        apellido: str,
        direccion: str,
        pais: str,
        estado: str,
        ciudad: str,
        codigo_postal: str,
        telefono: str,
        genero: str = "Mr",
        dia_nacimiento: Optional[str] = None,
        mes_nacimiento: Optional[str] = None,
        anio_nacimiento: Optional[str] = None,
    ) -> None:
        """Completa y envía el formulario de alta de una cuenta."""
        self.escribir("#form form[action='/signup'] input[name='name']", nombre)
        self.escribir("#form form[action='/signup'] input[name='email']", email)
        self.hacer_clic("#form button[data-qa='signup-button']")

        # El sitio presenta los datos personales después del primer paso.
        self.page.locator("#id_gender1" if genero == "Mr" else "#id_gender2").check()
        self.escribir("#password", password)

        # La fecha de nacimiento es opcional; se completa solo si se proporciona.
        if dia_nacimiento:
            self.page.locator("#days").select_option(dia_nacimiento)
        if mes_nacimiento:
            self.page.locator("#months").select_option(mes_nacimiento)
        if anio_nacimiento:
            self.page.locator("#years").select_option(anio_nacimiento)

        self.escribir("#first_name", nombre_persona)
        self.escribir("#last_name", apellido)
        self.escribir("#address1", direccion)
        self.page.locator("#country").select_option(label=pais)
        self.escribir("#state", estado)
        self.escribir("#city", ciudad)
        self.escribir("#zipcode", codigo_postal)
        self.escribir("#mobile_number", telefono)
        self.hacer_clic("button[data-qa='create-account']")
