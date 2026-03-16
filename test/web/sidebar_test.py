import re

from playwright.sync_api import expect

from web.Application import Application


def test_sidebar_navigation_to_runs(app: Application, login):
    app.projects_page.navigate()
    app.projects_page.verify_page_is_loaded()

    app.projects_page.get_projects()[0].click()

    app.project_page.side_bar.is_visible()
    app.project_page.side_bar.go_to_runs()

    app.project_page.side_bar.nav_item_is_active("Runs")
    expect(app.project_page.page).to_have_url(re.compile(r"/runs"))


def test_sidebar_navigation_to_analytics(app: Application, login):
    app.projects_page.navigate()
    app.projects_page.verify_page_is_loaded()

    app.projects_page.get_projects()[0].click()

    app.project_page.side_bar.is_visible()
    app.project_page.side_bar.go_to_analytics()

    app.project_page.side_bar.nav_item_is_active("Analytics")
    expect(app.project_page.page).to_have_url(re.compile(r"/analytics"))