from enum import Enum

from playwright.sync_api import Locator, expect


class ProjectCard:

    def __init__(self, card: Locator):
        self._card = card
        self._link = card.locator("a")
        self._title = card.locator("h3.text-gray-700")
        self._test_count = card.locator("p.text-gray-500.text-sm")
        self._avatars = card.locator("img.rounded-full")
        self._badges = card.locator(".project-badges")

    def link(self) -> str:
        return self._link.get_attribute('href')

    def title(self) -> str:
        return self._title.text_content().strip()

    def _test_count(self) -> str:
        return self._test_count.text_content().strip()

    def _badges_has(self, expected_badges : Badges):
        expect(self._badges).to_contain_text(expected_badges.value)

    def click(self):
        self._card.click()


class Badges(Enum):
    Demo = "Demo"
    Classical = "Classical"
    Pytest = "Pytest"
    BDD = "BDD"
    Cucumber = "Cucumber"
