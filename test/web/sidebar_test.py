import re

import pytest
from playwright.sync_api import BrowserContext, expect

from web.Application import Application


sidebar_nav_cases = [
    pytest.param("Tests",        r"/projects/[^/]+/$",   id="SB1_Tests"),
    pytest.param("Requirements", r"/requirements",       id="SB2_Requirements"),
    pytest.param("Runs",         r"/runs",               id="SB3_Runs"),
    pytest.param("Plans",        r"/plans",              id="SB4_Plans"),
    pytest.param("Steps",        r"/steps",              id="SB5_Steps"),
    pytest.param("Pulse",        r"/pulse",              id="SB6_Pulse"),
    pytest.param("Imports",      r"/imports",            id="SB7_Imports"),
    pytest.param("Analytics",    r"/analytics",          id="SB8_Analytics"),
    pytest.param("Branches",     r"/branches",           id="SB9_Branches"),
]


@pytest.fixture(scope="module")
def project_app(logged_context: BrowserContext) -> Application:
    p = logged_context.new_page()
    app = Application(p)
    app.projects_page.navigate()
    app.projects_page.switch_to_grid_view()
    app.projects_page.verify_page_is_loaded()
    app.projects_page.get_projects()[0].click()
    app.project_page.side_bar.is_visible()
    yield app
    p.close()


@pytest.mark.web
@pytest.mark.parametrize("tab_name,url_pattern", sidebar_nav_cases)
def test_sidebar_navigation(project_app: Application, tab_name: str, url_pattern: str):
    project_app.project_page.side_bar.go_to_nav_menu(tab_name)
    project_app.project_page.side_bar.nav_item_is_active(tab_name)
    expect(project_app.project_page.page).to_have_url(re.compile(url_pattern))