from playwright.sync_api import Page, Locator, expect


class ProjectPageHeader:
    def __init__(self, page: Page):
        self.page = page
        self.root = page.locator(".common-page-header")
        self.page_title = self.root.locator("h2", has_text="Projects")
        self.heading = self.root.get_by_role("heading", name="Projects")
        self.select_company = self.root.locator("#company_id")
        self.plan_badge = self.root.locator(".tooltip-project-plan")
        self.plan_name = self.plan_badge.locator("span").last
        self.input_search = self.root.locator("#search")
        self.btn_create = self.root.get_by_role("link", name="Create")
        self.btn_manage = self.root.get_by_role("link", name="Manage")
        self.btn_grid_view = self.root.locator("#grid-view")
        self.btn_table_view = self.root.locator("#table-view")

    def select_company_by_name(self, name: str) -> None:
        self.select_company.select_option(label=name)

    def check_selected_company(self, expected_value: str):
        expect(self.select_company.locator("option:checked")).to_have_text(expected_value)

    def search(self, query: str) -> None:
        self.input_search.fill(query)

    def clear_search(self) -> None:
        self.input_search.clear()

    def click_create(self) -> None:
        self.btn_create.click()

    def click_manage(self):
        self.btn_manage.click()

    def plan_name_should_be(self, expected_value: str):
        expect(self.plan_name).to_have_text(expected_value)