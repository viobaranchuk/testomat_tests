import os
from ast import List

from playwright.sync_api import Page, expect

from web.components.ProjectCard import ProjectCard
from web.components.ProjectPageHeader import ProjectPageHeader


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = ProjectPageHeader(page)
        self.root = page.locator("#content-desktop")

        self.success_message = page.locator(".common-flash-success-right p")
        self.info_message = page.locator(".common-flash-info-right p")

        self.grid_container = page.locator("#grid")
        self._project_cards = page.locator("#grid ul li a[href*= '/projects/']")
        self.table_view_grid = page.locator("#myTable")

    def navigate(self) -> "ProjectsPage":
        self.page.goto(os.getenv("BASE_APP_URL"))
        self.header.heading.wait_for(state="visible")
        return self

    def get_success_message(self) -> str:
        return self.success_message.text_content().strip()

    def verify_page_is_loaded(self):
        expect(self.header.page_title).to_be_visible()
        expect(self.grid_container).to_be_visible()

    def get_projects(self) -> List[ProjectCard]:
        return [ProjectCard(card) for card in self._project_cards.all()]

    def search_and_get_results(self, query: str) -> List[ProjectCard]:
        (self.header.search(query))
        self.page.wait_for_timeout(300)
        return self.get_projects()

    def switch_to_table_view(self):
        self.header.btn_table_view.click()

    def count_of_project_visible(self, expected_count: int):
        return expect(self._project_cards.filter(visible=True)).to_have_count(expected_count)

    def get_total_projects(self) -> int:
        return int(self.total_count.text_content())

    def get_project_by_title(self, title: str) -> ProjectCard:
        card = self._project_cards.filter(has=self.page.locator("h3", has_text=title)).first
        return ProjectCard(card)

    def verify_table_view(self):
        expect(self.table_view_grid).to_be_visible()
