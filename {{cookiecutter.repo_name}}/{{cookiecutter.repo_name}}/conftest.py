import os
from collections.abc import Generator

import pytest
from playwright.sync_api import BrowserContext, ConsoleMessage, Error, Page, Playwright


# See https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.hookspec.pytest_collection_modifyitems
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """
    Check if any tests are marked as integration and append the `vite` fixture to them if so.
    """
    for item in items:
        if item.get_closest_marker("integration"):
            item.fixturenames.append("vite")  # type: ignore


@pytest.fixture(scope="session")
def vite() -> None:
    import platform
    import subprocess
    import sys

    completed_process = subprocess.run(
        ["npm", "run", "build"],
        check=False,
        shell=platform.system() == "Windows",
    )
    if completed_process.returncode != 0:
        print(completed_process.stderr)
        sys.exit(-1)


@pytest.fixture(scope="session")
def playwright(playwright: Playwright) -> Generator[Playwright]:
    """Override of playwright fixture so we can set up for use with Django.

    Background: https://github.com/microsoft/playwright-python/issues/439
    """
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    yield playwright


@pytest.fixture
def context(context: BrowserContext) -> Generator[BrowserContext]:
    # Uncomment to disable or modify Playwright timeout
    # context.set_default_timeout(0)  # In milliseconds #noqa ERA001

    yield context


@pytest.fixture
def page(page: Page) -> Generator[Page]:
    """Override of playwright page fixture that raises any console errors."""
    page.on("console", raise_error)

    yield page


def raise_error(msg: ConsoleMessage) -> None:
    """Raise an error if a console error occurs.

    Args:
        msg (ConsoleMessage): A console message.
    Raises:
        Error: An error message.
    """
    if msg.type != "error":
        return

    raise Error(f"error: {msg.text}, {msg.location['url']}")
