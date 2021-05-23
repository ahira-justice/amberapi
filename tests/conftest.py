import pytest
import os

from app.domain.config import *
from app.domain.constants import *
from tests.utils import get_db, setup, clear_db_data


@pytest.hookimpl()
def pytest_sessionstart(session):
    setup()


@pytest.hookimpl()
def pytest_runtest_teardown(item, nextitem):
    db = get_db()
    clear_db_data(db)


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    if ENVIRONMENT == "TEST":
        os.remove(TEST_DATABASE_FILE)
