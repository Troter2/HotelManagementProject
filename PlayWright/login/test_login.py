import re
from playwright.sync_api import Page, expect


def test_login(page: Page) -> None:
    page.goto("http://localhost:8000/")
    page.get_by_role("button", name="Log in").click()
    page.get_by_label("Usuario").click()
    page.get_by_label("Usuario").fill("admin")
    page.get_by_label("Usuario").press("Tab")
    page.get_by_label("Contraseña").fill("admin")
    page.get_by_label("Contraseña").press("Enter")
    expect(page.get_by_role("button", name="Log Out")).to_be_visible()