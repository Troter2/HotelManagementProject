import re
from playwright.sync_api import Page, expect


def test_check_menu_in_receptionist_role(page: Page) -> None:
    page.goto("http://localhost:8000/")
    page.get_by_role("button", name="Log in").click()
    page.get_by_label("Usuario").click()
    page.get_by_label("Usuario").fill("reception")
    page.get_by_label("Contraseña").click()
    page.get_by_label("Contraseña").fill("admin")
    page.get_by_label("Contraseña").press("Enter")
