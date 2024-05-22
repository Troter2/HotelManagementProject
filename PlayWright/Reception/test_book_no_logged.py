import re
from playwright.sync_api import Page, expect


def test_book_no_logged(page: Page) -> None:
    page.goto("http://localhost:8000/")
    page.get_by_role("link", name="Reservar").click()
    page.get_by_placeholder("DNI").click()
    page.get_by_placeholder("DNI").fill("12312312a")
    page.get_by_placeholder("DNI").press("Tab")
    page.get_by_placeholder("Nombre").fill("test")
    page.get_by_placeholder("Nombre").press("Tab")
    page.get_by_placeholder("Apellidos").fill("test")
    page.get_by_placeholder("Apellidos").press("Tab")
    page.get_by_placeholder("Correo Electrónico").fill("test@test.es")
    page.get_by_placeholder("Correo Electrónico").press("Tab")
    page.get_by_placeholder("Teléfono").fill("123123123")
    page.get_by_placeholder("Fecha de Entrada ").fill("2024-10-22")
    page.get_by_placeholder("Fecha de Salida").fill("2024-10-24")
    page.get_by_placeholder("Número de Huéspedes").click()
    page.get_by_placeholder("Número de Huéspedes").fill("3")
    page.get_by_text("Volver Reservar DNI Nombre").click()
    page.get_by_role("button", name="Reservar").click()
    expect(page.get_by_role("button", name="Descargar Comprobante")).to_be_visible()
