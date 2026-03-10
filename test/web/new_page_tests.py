from faker import Faker
from playwright.sync_api import Page

from web.pages.NewProjectPage import NewProjectPage
from web.pages.ProjectPage import ProjectPage


def test_new_project_creation(page: Page, login):
    target_project_name = Faker().company()
    (NewProjectPage(page)
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (ProjectPage(page)
     .is_loaded()
     .close_readme()
     .project_name_is(target_project_name))