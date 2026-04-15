import time
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://demoqa.com/text-box")
    page.get_by_role("textbox", name="Full Name").click()
    page.get_by_role("textbox", name="Full Name").fill("reterterstrft")
    page.get_by_role("textbox", name="name@example.com").click()
    page.get_by_role("textbox", name="name@example.com").fill("ioledasz@mail.ru")
    page.get_by_role("textbox", name="Current Address").click()
    page.get_by_role("textbox", name="Current Address").fill("hmkfdsfcdf")
    page.locator("#permanentAddress").click()
    page.locator("#permanentAddress").fill("nsrthyagfzdgg")
    page.get_by_role("button", name="Submit").click()
    expect(page.locator("#name")).to_contain_text("Name:reterterstrft")
    expect(page.locator("#email")).to_contain_text("Email:ioledasz@mail.ru")
#g
    time.sleep(10)

