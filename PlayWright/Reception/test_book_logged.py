import re
from playwright.sync_api import Page, expect


def test_book_logged(page: Page) -> None:
    page.goto("http://localhost:8000/")
    page.get_by_role("button", name="Log in").click()
    page.get_by_label("Usuario").click()
    page.get_by_label("Usuario").fill("admin")
    page.get_by_label("Usuario").press("Tab")
    page.get_by_label("Contraseña").fill("admin")
    page.get_by_role("main").get_by_role("button", name="Log in").click()
    page.get_by_role("link", name="Reservar").click()
    page.get_by_placeholder("DNI").click()
    page.get_by_placeholder("DNI").fill("12345678H")
    page.get_by_placeholder("Apellidos").click()
    page.get_by_placeholder("Apellidos").fill("guti")
    page.get_by_placeholder("Fecha de Entrada ").fill("2024-12-12")
    page.get_by_placeholder("Fecha de Salida").fill("2024-12-25")
    page.get_by_placeholder("Número de Huéspedes").click()
    page.get_by_placeholder("Número de Huéspedes").fill("2")
    page.get_by_role("button", name="Reservar").click()
    #expect(page.get_by_role("button", name="Descargar Comprobante")).to_be_visible()