import pytest
from faker import Faker

from web.Application import Application

@pytest.mark.skip
def test_new_project_creation(logged_app: Application):
    target_project_name = Faker().company()

    (logged_app.new_project_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (logged_app.project_page
     .is_loaded()
     .close_readme()
     .project_name_is(target_project_name))

    (logged_app.project_page.side_bar
     .is_loaded()
     .click_logo()
     .expect_tab_active("Tests"))