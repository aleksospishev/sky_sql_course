import json
from unittest.mock import MagicMock

import pytest
import requests

from src.api_connect import HHAPIClient


# TEST HHAPIClient
@pytest.fixture
def mock_requests(monkeypatch):
    """фикстура."""

    def mock_get(url, *args, **kwargs):
        mock_response = MagicMock()
        if "employers" in url:
            if "12345" in url:
                mock_response.status_code = 200
                mock_response.json.return_value = {"id": 12345, "name": "Test Employer"}
            elif "67890" in url:
                mock_response.status_code = 200
                mock_response.json.return_value = {"id": 67890, "name": "Another Test Employer"}
            else:
                mock_response.status_code = 404
        elif "vacancies" in url:
            mock_response.status_code = 200
            mock_response.json.return_value = {"items": [{"id": 1, "name": "Test Vacancy"}], "pages": 1}
        return mock_response

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def hh_api_client():
    """фикстура."""
    return HHAPIClient()


@pytest.fixture
def temp_config_file(tmp_path):
    config_content = """
    [postgres]
    host = localhost
    port = 5432
    user = test_user
    password = test_password
    """
    config_file = tmp_path / "test_config.ini"
    config_file.write_text(config_content)
    return str(config_file)


@pytest.fixture
def temp_json_file(tmp_path):
    data = [1, 2, 3, 4, 5]
    file_path = tmp_path / "numbers.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file)
    return file_path
