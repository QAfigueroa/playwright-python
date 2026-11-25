from playwright.sync_api import expect

from pages.login_page import LoginPage


def test_login_con_credenciales_invalidas_muestra_error(
    login_page: LoginPage,
) -> None:
    """Verifica que el sitio informe cuando las credenciales no son válidas."""
    login_page.abrir()
    login_page.iniciar_sesion(
        email="usuario.inexistente@example.com",
        password="clave_incorrecta",
    )

    expect(
        login_page.obtener_elemento("#form p").filter(
            has_text="Your email or password is incorrect!"
        )
    ).to_be_visible()
    assert login_page.obtener_error_login() == (
        "Your email or password is incorrect!"
    )
