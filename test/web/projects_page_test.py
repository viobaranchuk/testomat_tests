from web.Application import Application
from web.components.ProjectCard import Badges


def test_projects_page_search(app: Application, login):
    app.projects_page.navigate()
    app.projects_page.verify_page_is_loaded()
    app.projects_page.header.select_company_by_name("QA Club Lviv")

    target_project_name = "PLY"
    app.projects_page.header.search(target_project_name)

    app.projects_page.count_of_project_visible(1)
    target_project = app.projects_page.get_project_by_title(target_project_name)
    target_project._badges_has(Badges.Classical)


def test_projects_page_table_view(app: Application, login):
    app.projects_page.navigate()
    app.projects_page.verify_page_is_loaded()

    app.projects_page.switch_to_table_view()
    app.projects_page.verify_table_view()