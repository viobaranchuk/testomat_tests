import re

import faker
from faker import Faker
from playwright.sync_api import Page, expect
from dotenv import load_dotenv

from test.conftest import Config

load_dotenv()

def test_login_with_invalid_pass(page: Page, configs: Config):
    open_login_page(page, configs)

    invalid_password = Faker().password(length=10)
    login_user(page, configs.email, invalid_password)


def test_search_project_in_company(page: Page, configs: Config):
    open_login_page(page, configs)
    login_user(page, configs.email, configs.password)
    target_project = "Books"
    search_for_project(page, target_project)

    expect(page.get_by_role("heading", name=target_project)).to_be_visible()
    expect(page.locator("ul li h3", has_text=target_project)).to_be_visible()


def search_for_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign In").click()

def open_login_page(page: Page, configs: Config):
    page.goto(f"{configs.base_app_url}/users/sign_in")

def test_should_be_possible_to_open_free_project(page: Page, configs: Config):
    open_login_page(page, configs)
    login_user(page, configs.email, configs.password)
    page.locator("#content-desktop #company_id").click()

    page.locator('#company_id').select_option(label='Free Projects')
    target_project = "Books"
    search_for_project(page, target_project)
    expect(page.get_by_role("heading", name=target_project)).to_be_hidden()

def test_create_and_delete_free_project(page: Page, configs: Config):
    project_name: str = faker.Faker().text(10)

    open_login_page(page, configs)
    login_user(page, configs.email, configs.password)
    page.locator("#content-desktop #company_id").click()

    page.locator('#company_id').select_option(label='Free Projects')

    page.locator("//*[@href='/projects/new']").last.click()
    expect(page.locator('#classical-img')).to_have_attribute('src', '/images/projects/circle-tick.svg')
    page.locator(' #project_title').fill(project_name)

    page.get_by_role("checkbox", name="Fill demo data").click()
    page.get_by_role("button", name="CucumberJS Demo Project").click()
    page.get_by_role("button", name="Create Demo").click()

    page.wait_for_url(re.compile(".*projects/cucumberjs-demo-project.*"))

def open_home_page(page: Page, configs: Config):
    page.goto(configs.base_url)