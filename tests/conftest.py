from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module

BASELINE_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture
def client():
    """Return a client with a clean in-memory activity state before each test."""
    app_module.activities = deepcopy(BASELINE_ACTIVITIES)
    with TestClient(app_module.app) as test_client:
        yield test_client
    app_module.activities = deepcopy(BASELINE_ACTIVITIES)
