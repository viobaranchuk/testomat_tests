from faker import Faker
from playwright.sync_api import Page

from web.Application import Application


def test_new_project_creation(page: Page, login, app: Application):
    target_project_name = Faker().company()

    (app.new_project_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (app.project_page
     .is_loaded()
     .close_readme()
     .project_name_is(target_project_name))

    (app.project_page.side_bar
     .is_loaded()
     .click_logo()
     .expect_tab_active("Tests"))