from playwright.sync_api import Page, expect
from pages.home_page import HomePage

"""
42 pruebas de Playwright (Python + pytest) para https://automationexercise.com

Cómo usarlo:
  1. Copia este archivo dentro de la carpeta tests/ de tu proyecto.
  2. Ejecuta todo:            pytest tests/test_automationexercise_42.py --headed
  3. Ejecuta un grupo:        pytest -k "carrito" --headed
  4. Ejecuta una sola prueba: pytest -k "test_09" --headed

Grupos de pruebas:
  - Página principal (01-08)
  - Navegación del menú (09-15)
  - Productos (16-23)
  - Carrito (24-28)
  - Login y registro (29-34)
  - Contacto (35-38)
  - Suscripción y otros (39-42)

Este archivo es independiente: no usa tus Page Objects, para que veas
cómo funciona Playwright "a pelo". Cada prueba tiene una descripción
(docstring) que explica qué verifica.
"""

import re
import uuid

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://automationexercise.com"


# ---------------------------------------------------------------------------
# FUNCIONES AUXILIARES (se reutilizan en varias pruebas)
# ---------------------------------------------------------------------------

def ir(page: Page, ruta: str = "") -> None:
    """Abre una página del sitio. Ejemplo: ir(page, '/products')."""
    page.goto(f"{BASE_URL}{ruta}")


def menu(page: Page):
    """Devuelve el menú de navegación superior para buscar enlaces dentro de él."""
    return page.locator(".navbar-nav")


def correo_unico() -> str:
    """Genera un correo distinto en cada ejecución para no repetir datos."""
    return f"qa_{uuid.uuid4().hex[:10]}@example.com"


def agregar_al_carrito(page: Page, indice: int = 0) -> None:
    """Agrega al carrito el producto número 'indice' de la lista (0 = el primero)."""
    tarjeta = page.locator(".features_items .product-image-wrapper").nth(indice)
    tarjeta.scroll_into_view_if_needed()
    tarjeta.hover()  # el botón "Add to cart" aparece al pasar el mouse
    tarjeta.locator(".product-overlay .add-to-cart").click()
    expect(page.locator("#cartModal")).to_be_visible()


@pytest.fixture(autouse=True)
def bloquear_anuncios(page: Page):
    """
    Se ejecuta automáticamente antes de cada prueba.
    Bloquea las peticiones a servidores de anuncios, que a veces tapan la
    página y hacen fallar las pruebas sin que haya un error real.
    """
    dominios = re.compile(
        r".*(?:googlesyndication|doubleclick|googleadservices|adservice).*"
    )
    page.route(dominios, lambda ruta: ruta.abort())
    yield


# ---------------------------------------------------------------------------
# GRUPO 1: PÁGINA PRINCIPAL (01-08)
# ---------------------------------------------------------------------------

def test_01_titulo_home(page: Page):
    """Verifica que la pestaña del navegador muestre el título 'Automation Exercise'."""
    ir(page)
    expect(page).to_have_title("Automation Exercise")


def test_02_logo_visible(page: Page):
    """Verifica que el logo del sitio se vea en la parte superior."""
    ir(page)
    expect(page.locator("img[alt='Website for automation practice']")).to_be_visible()


def test_03_menu_principal_visible(page: Page):
    """Verifica que los enlaces principales del menú estén visibles."""
    ir(page)
    for nombre in ["Home", "Products", "Cart", "Signup / Login",
                   "Test Cases", "API Testing", "Contact us"]:
        expect(menu(page).get_by_role("link", name=nombre)).to_be_visible()


def test_04_carrusel_visible(page: Page):
    """Verifica que el carrusel de banners de la página principal esté visible."""
    ir(page)
    expect(page.locator("#slider")).to_be_visible()


def test_05_features_items_visible(page: Page):
    """Verifica que exista la sección 'Features Items' con su título."""
    ir(page)
    expect(page.locator(".features_items h2.title")).to_have_text(
        "Features Items", ignore_case=True
    )


def test_06_categorias_visibles(page: Page):
    """Verifica que el panel lateral de categorías muestre Women, Men y Kids."""
    ir(page)
    panel = page.locator(".category-products")
    expect(panel).to_be_visible()
    for categoria in ["Women", "Men", "Kids"]:
        expect(panel).to_contain_text(categoria)


def test_07_marcas_visibles(page: Page):
    """Verifica que el panel lateral de marcas muestre algunas marcas conocidas."""
    ir(page)
    panel = page.locator(".brands_products")
    expect(panel).to_be_visible()
    for marca in ["Polo", "H&M", "Madame"]:
        expect(panel).to_contain_text(marca)


def test_08_seccion_recomendados(page: Page):
    """Verifica que exista la sección de 'recommended items' (productos recomendados)."""
    ir(page)
    expect(page.locator(".recommended_items")).to_contain_text(
        "recommended items", ignore_case=True
    )


# ---------------------------------------------------------------------------
# GRUPO 2: NAVEGACIÓN DEL MENÚ (09-15)
# ---------------------------------------------------------------------------

def test_09_ir_a_productos(page: Page):
    """Hace clic en 'Products' y verifica que se abra la página 'All Products'."""
    ir(page)
    menu(page).get_by_role("link", name="Products").click()
    expect(page).to_have_url(re.compile(r"/products$"))
    expect(page.locator("h2.title")).to_contain_text("All Products", ignore_case=True)


def test_10_ir_a_carrito(page: Page):
    """Hace clic en 'Cart' y verifica que se abra la página del carrito."""
    ir(page)
    menu(page).get_by_role("link", name="Cart").click()
    expect(page).to_have_url(re.compile(r"/view_cart$"))


def test_11_ir_a_login(page: Page):
    """Hace clic en 'Signup / Login' y verifica que se abra la página de acceso."""
    ir(page)
    menu(page).get_by_role("link", name="Signup / Login").click()
    expect(page).to_have_url(re.compile(r"/login$"))


def test_12_ir_a_test_cases(page: Page):
    """Hace clic en 'Test Cases' y verifica que se abra esa página con su título."""
    ir(page)
    menu(page).get_by_role("link", name="Test Cases").click()
    expect(page).to_have_url(re.compile(r"/test_cases$"))
    expect(page.locator("h2.title")).to_contain_text("Test Cases", ignore_case=True)


def test_13_ir_a_api_testing(page: Page):
    """Hace clic en 'API Testing' y verifica que se abra la lista de APIs."""
    ir(page)
    menu(page).get_by_role("link", name="API Testing").click()
    expect(page).to_have_url(re.compile(r"/api_list$"))
    expect(page.locator("h2.title")).to_contain_text("APIs List", ignore_case=True)


def test_14_ir_a_contacto(page: Page):
    """Hace clic en 'Contact us' y verifica que se abra el formulario 'Get In Touch'."""
    ir(page)
    menu(page).get_by_role("link", name="Contact us").click()
    expect(page).to_have_url(re.compile(r"/contact_us$"))
    expect(page.get_by_role("heading", name="Get In Touch", exact=True)).to_be_visible()


def test_15_volver_al_home(page: Page):
    """Desde la página de productos, hace clic en 'Home' y verifica que regrese al inicio."""
    ir(page, "/products")
    menu(page).get_by_role("link", name="Home").click()
    expect(page).to_have_url(re.compile(r"automationexercise\.com/?$"))


# ---------------------------------------------------------------------------
# GRUPO 3: PRODUCTOS (16-23)
# ---------------------------------------------------------------------------

def test_16_lista_de_productos(page: Page):
    """Verifica que la página de productos muestre al menos un producto."""
    ir(page, "/products")
    tarjetas = page.locator(".features_items .product-image-wrapper")
    expect(tarjetas.first).to_be_visible()
    assert tarjetas.count() > 0


def test_17_buscar_producto_existente(page: Page):
    """Busca 'Tshirt' y verifica que aparezcan resultados en 'Searched Products'."""
    ir(page, "/products")
    page.fill("#search_product", "Tshirt")
    page.click("#submit_search")
    expect(page.locator("h2.title")).to_contain_text("Searched Products", ignore_case=True)
    expect(page.locator(".features_items .product-image-wrapper").first).to_be_visible()


def test_18_buscar_producto_inexistente(page: Page):
    """Busca un texto absurdo y verifica que no aparezca ningún producto."""
    ir(page, "/products")
    page.fill("#search_product", "zzzxxxqqq")
    page.click("#submit_search")
    expect(page.locator("h2.title")).to_contain_text("Searched Products", ignore_case=True)
    expect(page.locator(".features_items .product-image-wrapper")).to_have_count(0)


def test_19_abrir_detalle_de_producto(page: Page):
    """Hace clic en 'View Product' del primer producto y verifica que abra su detalle."""
    ir(page, "/products")
    page.locator("a[href^='/product_details/']").first.click()
    expect(page).to_have_url(re.compile(r"/product_details/\d+"))
    expect(page.locator(".product-information")).to_be_visible()


def test_20_detalle_muestra_datos(page: Page):
    """Abre el producto 1 y verifica nombre, categoría, disponibilidad, condición y marca."""
    ir(page, "/product_details/1")
    info = page.locator(".product-information")
    expect(info.locator("h2")).to_contain_text("Blue Top")
    for dato in ["Category:", "Availability:", "Condition:", "Brand:"]:
        expect(info).to_contain_text(dato)


def test_21_filtrar_por_categoria(page: Page):
    """Despliega 'Women', elige 'Dress' y verifica que el título sea 'Women - Dress Products'."""
    ir(page, "/products")
    page.locator("a[href='#Women']").click()
    page.locator("a[href='/category_products/1']").click()
    expect(page).to_have_url(re.compile(r"/category_products/1$"))
    expect(page.locator(".features_items h2.title")).to_contain_text(
        "Women - Dress Products", ignore_case=True
    )


def test_22_filtrar_por_marca(page: Page):
    """Hace clic en la marca 'Polo' y verifica que el título sea 'Brand - Polo Products'."""
    ir(page, "/products")
    page.locator(".brands_products a[href='/brand_products/Polo']").click()
    expect(page).to_have_url(re.compile(r"/brand_products/Polo$"))
    expect(page.locator(".features_items h2.title")).to_contain_text(
        "Brand - Polo Products", ignore_case=True
    )


def test_23_cambiar_cantidad_en_detalle(page: Page):
    """En el detalle de un producto, cambia la cantidad a 4 y verifica que el campo la conserve."""
    ir(page, "/product_details/1")
    page.fill("#quantity", "4")
    expect(page.locator("#quantity")).to_have_value("4")


# ---------------------------------------------------------------------------
# GRUPO 4: CARRITO (24-28)
# ---------------------------------------------------------------------------

def test_24_carrito_vacio(page: Page):
    """Con una sesión nueva, verifica que el carrito muestre el mensaje 'Cart is empty!'."""
    ir(page, "/view_cart")
    expect(page.locator("#empty_cart")).to_be_visible()
    expect(page.locator("#empty_cart")).to_contain_text("Cart is empty!")


def test_25_agregar_producto_desde_lista(page: Page):
    """Agrega el primer producto desde la lista y verifica el mensaje 'Added!' en la ventana emergente."""
    ir(page, "/products")
    agregar_al_carrito(page, 0)
    expect(page.locator("#cartModal")).to_contain_text("Added!")


def test_26_ver_carrito_tras_agregar(page: Page):
    """Agrega un producto, entra a 'View Cart' y verifica que haya exactamente 1 fila."""
    ir(page, "/products")
    agregar_al_carrito(page, 0)
    page.locator("#cartModal").get_by_role("link", name="View Cart").click()
    expect(page).to_have_url(re.compile(r"/view_cart$"))
    expect(page.locator("#cart_info_table tbody tr")).to_have_count(1)


def test_27_agregar_dos_productos(page: Page):
    """Agrega dos productos distintos y verifica que el carrito tenga 2 filas."""
    ir(page, "/products")
    agregar_al_carrito(page, 0)
    page.get_by_role("button", name="Continue Shopping").click()
    expect(page.locator("#cartModal")).to_be_hidden()
    agregar_al_carrito(page, 1)
    page.locator("#cartModal").get_by_role("link", name="View Cart").click()
    expect(page.locator("#cart_info_table tbody tr")).to_have_count(2)


def test_28_eliminar_producto_del_carrito(page: Page):
    """Agrega un producto, lo elimina con la 'X' y verifica que el carrito quede vacío."""
    ir(page, "/products")
    agregar_al_carrito(page, 0)
    page.locator("#cartModal").get_by_role("link", name="View Cart").click()
    # Espera a que cart.js registre el manejador antes de interactuar con el botón.
    page.wait_for_function(
        """() => {
            const boton = document.querySelector('.cart_quantity_delete');
            const eventos = window.jQuery && boton && window.jQuery._data(boton, 'events');
            return Boolean(eventos && eventos.click && eventos.click.length);
        }"""
    )
    page.locator(".cart_quantity_delete").first.click()
    # La fila desaparece cuando el servidor termina la eliminación asíncrona.
    expect(page.locator("#cart_info_table tbody tr")).to_have_count(0, timeout=10000)
    expect(page.locator("#empty_cart")).to_be_visible()


# ---------------------------------------------------------------------------
# GRUPO 5: LOGIN Y REGISTRO (29-34)
# ---------------------------------------------------------------------------

def test_29_formulario_login_visible(page: Page):
    """Verifica que el formulario de login muestre su título, correo, contraseña y botón."""
    ir(page, "/login")
    expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()
    expect(page.locator("[data-qa='login-email']")).to_be_visible()
    expect(page.locator("[data-qa='login-password']")).to_be_visible()
    expect(page.locator("[data-qa='login-button']")).to_be_visible()


def test_30_formulario_signup_visible(page: Page):
    """Verifica que el formulario de registro muestre su título, nombre, correo y botón."""
    ir(page, "/login")
    expect(page.get_by_role("heading", name="New User Signup!")).to_be_visible()
    expect(page.locator("[data-qa='signup-name']")).to_be_visible()
    expect(page.locator("[data-qa='signup-email']")).to_be_visible()
    expect(page.locator("[data-qa='signup-button']")).to_be_visible()


def test_31_login_con_credenciales_invalidas(page: Page):
    """Intenta iniciar sesión con un usuario inventado y verifica el mensaje de error."""
    ir(page, "/login")
    page.fill("[data-qa='login-email']", correo_unico())
    page.fill("[data-qa='login-password']", "clave_incorrecta")
    page.click("[data-qa='login-button']")
    expect(page.get_by_text("Your email or password is incorrect!")).to_be_visible()


def test_32_login_con_campos_vacios(page: Page):
    """Pulsa 'Login' sin llenar nada y verifica que el navegador marque el correo como obligatorio."""
    ir(page, "/login")
    page.click("[data-qa='login-button']")
    expect(page).to_have_url(re.compile(r"/login$"))
    campo_vacio = page.locator("[data-qa='login-email']").evaluate(
        "el => el.validity.valueMissing"
    )
    assert campo_vacio is True


def test_33_signup_con_correo_nuevo(page: Page):
    """Registra nombre y correo nuevos y verifica que avance a 'Enter Account Information'."""
    ir(page, "/login")
    page.fill("[data-qa='signup-name']", "Tester QA")
    page.fill("[data-qa='signup-email']", correo_unico())
    page.click("[data-qa='signup-button']")
    expect(page).to_have_url(re.compile(r"/signup$"))
    expect(page.get_by_text("Enter Account Information")).to_be_visible()


def test_34_signup_con_campos_vacios(page: Page):
    """Pulsa 'Signup' sin llenar nada y verifica que el nombre quede marcado como obligatorio."""
    ir(page, "/login")
    page.click("[data-qa='signup-button']")
    expect(page).to_have_url(re.compile(r"/login$"))
    campo_vacio = page.locator("[data-qa='signup-name']").evaluate(
        "el => el.validity.valueMissing"
    )
    assert campo_vacio is True


# ---------------------------------------------------------------------------
# GRUPO 6: CONTACTO (35-38)
# ---------------------------------------------------------------------------

def test_35_formulario_contacto_visible(page: Page):
    """Verifica que el formulario de contacto muestre todos sus campos y el botón de envío."""
    ir(page, "/contact_us")
    expect(page.get_by_role("heading", name="Get In Touch", exact=True)).to_be_visible()
    for campo in ["name", "email", "subject", "message", "submit-button"]:
        expect(page.locator(f"[data-qa='{campo}']")).to_be_visible()


def test_36_enviar_formulario_contacto(page: Page):
    """Llena el formulario, acepta la alerta del navegador y verifica el mensaje de éxito."""
    ir(page, "/contact_us")
    page.fill("[data-qa='name']", "Tester QA")
    page.fill("[data-qa='email']", correo_unico())
    page.fill("[data-qa='subject']", "Prueba automatizada")
    page.fill("[data-qa='message']", "Este mensaje fue enviado con Playwright.")
    page.once("dialog", lambda dialogo: dialogo.accept())  # acepta el "OK" de la alerta
    page.click("[data-qa='submit-button']")
    expect(page.locator(".status.alert-success")).to_contain_text(
        "Success! Your details have been submitted successfully."
    )


def test_37_contacto_con_campos_vacios(page: Page):
    """Pulsa 'Submit' sin llenar nada y verifica que el correo obligatorio se marque."""
    ir(page, "/contact_us")
    page.click("[data-qa='submit-button']")
    expect(page).to_have_url(re.compile(r"/contact_us$"))
    campo_vacio = page.locator("[data-qa='email']").evaluate(
        "el => el.validity.valueMissing"
    )
    assert campo_vacio is True


def test_38_adjuntar_archivo_en_contacto(page: Page, tmp_path):
    """Crea un archivo temporal, lo adjunta al formulario y verifica que el campo lo reconozca."""
    archivo = tmp_path / "prueba.txt"
    archivo.write_text("archivo de prueba")
    ir(page, "/contact_us")
    page.set_input_files("input[name='upload_file']", str(archivo))
    nombre = page.locator("input[name='upload_file']").evaluate(
        "el => el.files[0].name"
    )
    assert nombre == "prueba.txt"


# ---------------------------------------------------------------------------
# GRUPO 7: SUSCRIPCIÓN Y OTROS (39-42)
# ---------------------------------------------------------------------------

def test_39_suscripcion_con_correo_valido(page: Page):
    """Escribe un correo en la suscripción del pie de página y verifica el mensaje de éxito."""
    ir(page)
    page.locator("#susbscribe_email").scroll_into_view_if_needed()
    page.fill("#susbscribe_email", correo_unico())
    page.click("#subscribe")
    expect(page.get_by_text("You have been successfully subscribed!")).to_be_visible()


def test_40_seccion_suscripcion_visible(page: Page):
    """Verifica que el pie de página muestre la sección 'Subscription' con su campo y botón."""
    ir(page)
    expect(page.get_by_role("heading", name="Subscription")).to_be_visible()
    expect(page.locator("#susbscribe_email")).to_be_visible()
    expect(page.locator("#subscribe")).to_be_visible()


def test_41_boton_volver_arriba(page: Page):
    """Baja hasta el final de la página, pulsa la flecha de 'volver arriba' y verifica que suba."""
    ir(page)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.locator("#scrollUp").click()
    page.wait_for_function("window.scrollY < 100")
    assert page.evaluate("window.scrollY") < 100


def test_42_lista_de_apis_contenido(page: Page):
    """Abre la lista de APIs y verifica que describa 'API 1' y el código de respuesta 200."""
    ir(page, "/api_list")
    cuerpo = page.locator("body")
    expect(cuerpo).to_contain_text("API 1: Get All Products List")
    expect(cuerpo).to_contain_text("Response Code: 200")