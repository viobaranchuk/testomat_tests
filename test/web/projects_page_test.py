import pytest
from playwright.sync_api import Page

from web.components.ProjectCard import Badges
from web.pages.ProjectsPage import ProjectsPage


def test_projects_page_search(page: Page, login):
    projects_page = ProjectsPage(page)
    projects_page.navigate()

    projects_page.verify_page_is_loaded()
    projects_page.header.select_company_by_name("QA Club Lviv")

    target_project_name = "PLY"
    projects_page.header.search(target_project_name)

    projects_page.count_of_project_visible(1)
    target_project = projects_page.get_project_by_title(target_project_name)
    target_project._badges_has(Badges.Classical)


def test_projects_page_table_view(page: Page, login):
    projects_page = ProjectsPage(page)
    projects_page.navigate()

    projects_page.verify_page_is_loaded()

    projects_page.switch_to_table_view()
    projects_page.verify_table_view()
