import re
from typing import Self

from playwright.sync_api import Page, Locator, expect


class SideBar:
    def __init__(self, page: Page):
        self.page = page
        self.root = page.locator(".mainnav-menu-body")

        self.logo = self.root.locator("button.btn-open")
        self.btn_close = self.root.get_by_role("button")

        self.nav_tests = self.root.get_by_role("link", name="Tests")
        self.nav_requirements = self.root.get_by_role("link", name="Requirements")
        self.nav_runs = self.root.get_by_role("link", name="Runs")
        self.nav_plans = self.root.get_by_role("link", name="Plans")
        self.nav_steps = self.root.get_by_role("link", name="Steps")
        self.nav_pulse = self.root.get_by_role("link", name="Pulse")
        self.nav_imports = self.root.get_by_role("link", name="Imports")
        self.nav_analytics = self.root.get_by_role("link", name="Analytics")
        self.nav_branches = self.root.get_by_role("link", name="Branches")
        self.nav_settings = self.root.get_by_role("link", name="Settings")

    def is_loaded(self) -> Self:
        expect(self.root).to_be_visible()
        expect(self.logo).to_be_visible()
        # expect(self.nav_tests).to_be_visible()
        # expect(self.nav_settings).to_be_visible()
        return self

    def is_visible(self) -> Self:
        expect(self.root).to_be_visible()
        return self

    def nav_item_is_active(self, name: str) -> Self:
        nav_item = self.root.get_by_role("link", name=name)
        expect(nav_item).to_have_class(re.compile(r"active"))
        return self

    def expect_tab_active(self, name: str) -> Self:
        nav_item = self.root.get_by_role("link", name=name)
        expect(nav_item).to_have_class(re.compile(r"active"))
        return self

    def get_active_nav_item(self) -> Locator:
        return self.root.locator(".nav-item.active")

    def go_to_tests(self) -> Self:
        self.nav_tests.click()
        return self

    def go_to_requirements(self) -> Self:
        self.nav_requirements.click()
        return self

    def go_to_runs(self) -> Self:
        self.nav_runs.click()
        return self

    def go_to_plans(self) -> Self:
        self.nav_plans.click()
        return self

    def go_to_steps(self) -> Self:
        self.nav_steps.click()
        return self

    def go_to_pulse(self) -> Self:
        self.nav_pulse.click()
        return self

    def go_to_imports(self) -> Self:
        self.nav_imports.click()
        return self

    def go_to_analytics(self) -> Self:
        self.nav_analytics.click()
        return self

    def go_to_branches(self) -> Self:
        self.nav_branches.click()
        return self

    def go_to_settings(self) -> Self:
        self.nav_settings.click()
        return self

    def click_logo(self) -> Self:
        self.logo.click()
        return self