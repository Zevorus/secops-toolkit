import pytest
from unittest.mock import MagicMock
from secops_toolkit.clients import SecOpsClient

@pytest.fixture
def mock_secops_client():
    client = SecOpsClient()
    # Mocking individual secops_feature_clients sessions
    client.rules.session = MagicMock()
    client.tables.session = MagicMock()
    client.reference_lists.session = MagicMock()
    return client

def test_secops_list_rules(mock_secops_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rules": [{"name": "test_rule"}]}
    mock_response.status_code = 200
    mock_secops_client.rules.session.request.return_value = mock_response
    
    rules = mock_secops_client.rules.list_rules()
    assert rules is not None
    assert "rules" in rules
    assert rules["rules"][0]["name"] == "test_rule"

def test_secops_list_tables(mock_secops_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"dataTables": [{"id": "table_1"}]}
    mock_response.status_code = 200
    mock_secops_client.tables.session.request.return_value = mock_response
    
    tables = mock_secops_client.tables.list_tables()
    assert tables is not None
    assert "dataTables" in tables
    assert tables["dataTables"][0]["id"] == "table_1"
