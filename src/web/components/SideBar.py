import re
from typing import Self

from playwright.sync_api import Page, expect


_NAV_SELECTORS = {
    "Tests":        "a.nav-item[href*='/projects/'][href$='/']",
    "Requirements": "a.nav-item[href$='/requirements']",
    "Runs":         "a.nav-item[href$='/runs']",
    "Plans":        "a.nav-item[href$='/plans']",
    "Steps":        "a.nav-item[href$='/steps']",
    "Pulse":        "a.nav-item[href$='/pulse']",
    "Imports":      "a.nav-item[href$='/imports']",
    "Analytics":    "a.nav-item[href$='/analytics']",
    "Branches":     "a.nav-item[href$='/branches']",
    "Settings":     "a.nav-item[href='#']",
}


class SideBar:
    def __init__(self, page: Page):
        self.page = page
        self.root = page.locator(".mainnav-menu-body")
        self.logo = self.root.locator("button.btn-open")

    def is_loaded(self) -> Self:
        expect(self.root).to_be_visible()
        expect(self.logo).to_be_visible()
        return self

    def is_visible(self) -> Self:
        expect(self.root).to_be_visible()
        return self

    def go_to_nav_menu(self, menu: str) -> Self:
        self.root.locator(_NAV_SELECTORS[menu]).click()
        return self

    def nav_item_is_active(self, name: str) -> Self:
        expect(self.root.locator(_NAV_SELECTORS[name])).to_have_class(re.compile(r"active"))
        return self

    def expect_tab_active(self, name: str) -> Self:
        expect(self.root.locator(_NAV_SELECTORS[name])).to_have_class(re.compile(r"active"))
        return self

    def click_logo(self) -> Self:
        self.logo.click()
        return self