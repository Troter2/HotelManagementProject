import re
from playwright.sync_api import Page, expect


def test_go_booking_from_rooms(page: Page) -> None:
    page.goto("http://localhost:8000/")
    page.get_by_role("link", name="Habitaciones", exact=True).click()
    page.get_by_role("link", name="Reservar").nth(1).click()
    page.get_by_placeholder("DNI").click()