import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.parametrize("return_value,expected_valid,expected_post_code", [
    ("POSTCODE", True, "POSTCODE"),
    (False, False, None)
])
@patch('main.validate_post_code')
def test_validate_post_code(mock_validate_post_code, return_value, expected_valid, expected_post_code):
    mock_validate_post_code.return_value = return_value
    response = client.post("/v1/validate", json={"post_code": "POSTCODE", "strict": True})
    assert response.status_code == 200
    assert "X-Correlation-Id" in response.headers
    assert response.json()["valid"] is expected_valid
    assert response.json()["post_code"] == expected_post_code
