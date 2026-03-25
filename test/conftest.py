import base64
import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, BrowserContext, Browser, sync_playwright
from pytest_html import extras as html_extras

from web.Application import Application
from web.pages.LoginPage import LoginPage


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"_report_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        page = getattr(item, "_current_page", None)
        if page:
            try:
                screenshot_bytes = page.screenshot(full_page=True)
                rep.extras = getattr(rep, "extras", []) + [
                    html_extras.png(base64.b64encode(screenshot_bytes).decode())
                ]
            except Exception:
                pass

load_dotenv()

_CONTEXT_OPTIONS = {
    "base_url": "https://app.testomat.io",
    "viewport": {"width": 1512, "height": 982},
    "locale": "en_SE",
    "timezone_id": "Europe/Berlin",
    "record_video_dir": "videos/",
    "permissions": ["geolocation"],
}


@dataclass(frozen=True)
class Config:
    base_url: str
    base_app_url: str
    login_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs() -> Config:
    return Config(
        base_url=os.getenv("BASE_URL"),
        base_app_url=os.getenv("BASE_APP_URL"),
        login_url=os.getenv("LOGIN_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
    )


# ── Browser (one per session) ─────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100, timeout=30000)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def context(browser: Browser) -> BrowserContext:
    ctx = browser.new_context(**_CONTEXT_OPTIONS)
    yield ctx
    ctx.close()


_TRACES_DIR = "test-result/traces"


def _test_failed(request: pytest.FixtureRequest) -> bool:
    report = getattr(request.node, "_report_call", None)
    return report is not None and report.failed


def _safe_name(request: pytest.FixtureRequest) -> str:
    return request.node.nodeid.replace("/", "_").replace("::", "_").replace(" ", "_")


def _stop_tracing(ctx: BrowserContext, request: pytest.FixtureRequest) -> None:
    if _test_failed(request):
        try:
            os.makedirs(_TRACES_DIR, exist_ok=True)
            ctx.tracing.stop(path=f"{_TRACES_DIR}/{_safe_name(request)}.zip")
        except Exception:
            pass
    else:
        try:
            ctx.tracing.stop()
        except Exception:
            pass


# ── Clean app — new page per test, shared context ─────────────────────────────

@pytest.fixture(scope="function")
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Page:
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    p = context.new_page()
    request.node._current_page = p
    yield p
    request.node._current_page = None
    _stop_tracing(context, request)
    context.clear_cookies()
    if not p.url.startswith("about:"):
        try:
            p.evaluate("window.localStorage.clear()")
            p.evaluate("window.sessionStorage.clear()")
        except Exception:
            pass
    p.close()


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


# ── Shared context for parametrized tests (module scope) ─────────────────────

@pytest.fixture(scope="module")
def shared_context(browser: Browser) -> BrowserContext:
    ctx = browser.new_context(**_CONTEXT_OPTIONS)
    yield ctx
    ctx.close()


@pytest.fixture(scope="module")
def shared_app(shared_context: BrowserContext) -> Application:
    p = shared_context.new_page()
    yield Application(p)
    p.close()


def clear_browser_state(page: Page) -> None:
    page.context.clear_cookies()
    if not page.url.startswith("about:"):
        page.evaluate("window.localStorage.clear()")
        page.evaluate("window.sessionStorage.clear()")


# ── Logged app — separate context, login performed once per session ───────────

@pytest.fixture(scope="session")
def logged_context(browser: Browser, configs: Config) -> BrowserContext:
    ctx = browser.new_context(**_CONTEXT_OPTIONS)
    p = ctx.new_page()
    login_page = LoginPage(p)
    login_page.open()
    login_page.is_loaded()
    login_page.login_user(configs.email, configs.password)
    p.close()
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def logged_page(logged_context: BrowserContext, request: pytest.FixtureRequest) -> Page:
    logged_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    p = logged_context.new_page()
    request.node._current_page = p
    yield p
    request.node._current_page = None
    _stop_tracing(logged_context, request)
    p.close()


@pytest.fixture(scope="function")
def logged_app(logged_page: Page) -> Application:
    return Application(logged_page)


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login_user(configs.email, configs.password)