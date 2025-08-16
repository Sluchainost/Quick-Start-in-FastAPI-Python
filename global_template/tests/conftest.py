""" DOC """

import pytest

from fastapi.testclient import TestClient

from global_template.app.main import app


@pytest.fixture
def client() -> TestClient:
    """ DOC """

    return TestClient(app)
