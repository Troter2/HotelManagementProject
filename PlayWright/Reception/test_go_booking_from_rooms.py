import re
from playwright.sync_api import Page, expect
import time



def test_go_booking_from_rooms(page: Page) -> None:
    page.goto("http://localhost:8000/")
    page.get_by_role("link", name="Habitaciones", exact=True).click()
    page.get_by_role("link", name="Reservar").nth(1).click()
    time.sleep(1)
    page.get_by_placeholder("Fecha de Entrada ").fill("2024-12-12")
    page.get_by_placeholder("Fecha de Entrada ").press("Enter")
    page.get_by_placeholder("Fecha de Salida").fill("2024-12-25")
    page.get_by_placeholder("Número de Huéspedes").click()
    page.get_by_placeholder("Número de Huéspedes").fill("2")
    page.get_by_role("button", name="Reservar").click()
