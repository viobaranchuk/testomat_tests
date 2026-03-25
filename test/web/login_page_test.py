import pytest
from faker import Faker

from test.conftest import Config, clear_browser_state
from web.Application import Application

_fake = Faker()

_PASSWORD_MIN = 6

invalid_login_cases = [
    # Equivalence Class Partitioning — email partitions
    pytest.param(_fake.email(),     _fake.password(length=10),                                                                      id="EC1_wrong_credentials"),
    pytest.param(_fake.user_name(), _fake.password(length=10),                                                                      id="EC2_no_at_sign"),
    pytest.param(f"@{_fake.domain_name()}", _fake.password(length=10),                                                             id="EC3_missing_local_part"),
    pytest.param(f"{_fake.user_name()}@", _fake.password(length=10),                                                               id="EC4_missing_domain"),
    pytest.param("", _fake.password(length=10),                                                                                     id="EC5_empty_email"),
    pytest.param(_fake.email(), "",                                                                                                  id="EC6_empty_password"),
    # Boundary Value Analysis — password length (min = 6)
    pytest.param(_fake.email(), _fake.password(length=_PASSWORD_MIN - 1, special_chars=False, digits=False, upper_case=False),      id="BVA1_password_below_min"),
    pytest.param(_fake.email(), _fake.password(length=_PASSWORD_MIN,     special_chars=False),                                     id="BVA2_password_at_min"),
    pytest.param(_fake.email(), _fake.password(length=_PASSWORD_MIN + 1, special_chars=False),                                     id="BVA3_password_above_min"),
    # SQL Injection — email field
    pytest.param("admin'--", _fake.password(length=10),                                                                            id="SEC2_sql_injection_comment"),
    pytest.param("' OR 1=1; DROP TABLE users;--", _fake.password(length=10),                                                       id="SEC3_sql_injection_drop"),
    # XSS — email field
    pytest.param("<img src=x onerror=alert(1)>", _fake.password(length=10),                                                        id="SEC5_xss_img_tag"),
    pytest.param("javascript:alert('xss')", _fake.password(length=10),                                                             id="SEC6_xss_javascript_protocol"),
    # SQL Injection — password field
    pytest.param(_fake.email(), "' OR '1'='1",                                                                                     id="SEC7_sql_injection_password_basic"),
    pytest.param(_fake.email(), "'; DROP TABLE users;--",                                                                          id="SEC9_sql_injection_password_drop"),
    # XSS — password field
    pytest.param(_fake.email(), "<script>alert('xss')</script>",                                                                   id="SEC10_xss_password_script_tag"),
    pytest.param(_fake.email(), "javascript:alert('xss')",                                                                         id="SEC12_xss_password_javascript_protocol"),
]

@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize("email,password", invalid_login_cases)
def test_login_invalid(shared_app: Application, email: str, password: str):
    shared_app.login_page.open()
    shared_app.login_page.is_loaded()
    shared_app.login_page.login_user(email, password)
    shared_app.login_page.invalid_login_message_visible()
    clear_browser_state(shared_app.page)
    shared_app.page.wait_for_timeout(5000)

@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(app: Application, configs: Config):
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    app.projects_page.verify_page_is_loaded()