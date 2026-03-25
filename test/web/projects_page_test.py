from web.Application import Application
from web.components.ProjectCard import Badges


def test_projects_page_search(logged_app: Application):
    logged_app.projects_page.navigate()
    logged_app.projects_page.verify_page_is_loaded()
    logged_app.projects_page.header.select_company_by_name("QA Club Lviv")

    target_project_name = "PLY"
    logged_app.projects_page.header.search(target_project_name)

    logged_app.projects_page.count_of_project_visible(1)
    target_project = logged_app.projects_page.get_project_by_title(target_project_name)
    target_project._badges_has(Badges.Classical)


def test_projects_page_table_view_switch(logged_app: Application):
    logged_app.projects_page.navigate()
    logged_app.projects_page.verify_page_is_loaded()

    logged_app.projects_page.switch_to_table_view()
    logged_app.projects_page.verify_table_view()

    logged_app.projects_page.switch_to_grid_view()
    logged_app.projects_page.verify_grid_view()