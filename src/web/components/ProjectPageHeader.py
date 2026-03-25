from playwright.sync_api import Page, Locator, expect


class ProjectPageHeader:
    def __init__(self, page: Page):
        self.page = page
        self._left = page.locator(".common-page-header-left")
        self.page_title = self._left.locator("h2", has_text="Projects")
        self.heading = self._left.locator("h2", has_text="Projects")
        self.select_company = self._left.locator("#company_id")
        self.plan_badge = self._left.locator(".tooltip-project-plan")
        self.plan_name = self.plan_badge.locator("span").last
        self.input_search = page.locator("#search")
        self.btn_create = page.get_by_role("link", name="Create")
        self.btn_manage = page.get_by_role("link", name="Manage")
        self.btn_grid_view = page.locator("#grid-view")
        self.btn_table_view = page.locator("#table-view")

    def select_company_by_name(self, name: str) -> None:
        self.select_company.select_option(label=name)

    def check_selected_company(self, expected_value: str):
        expect(self.select_company.locator("option:checked")).to_have_text(expected_value)

    def search(self, query: str) -> None:
        self.input_search.type(query)

    def clear_search(self) -> None:
        self.input_search.clear()

    def click_create(self) -> None:
        self.btn_create.click()

    def click_manage(self):
        self.btn_manage.click()

    def plan_name_should_be(self, expected_value: str):
        expect(self.plan_name).to_have_text(expected_value)