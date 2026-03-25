import pytest
from unittest.mock import MagicMock
from secops_toolkit.clients import SecOpsClient
from secops_toolkit.model.secops.rules_model import RuleList, RuleDeployment


@pytest.fixture
def mock_secops_client():
    client = SecOpsClient()
    # Mocking individual secops_feature_clients sessions
    client.rules.session = MagicMock()
    return client


def test_secops_list_rules(mock_secops_client):
    # Mock Response for RuleList
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "rules": [{"name": "projects/123/locations/us/instances/abc/rules/rule_1", "displayName": "test_rule"}],
        "nextPageToken": "token_123"
    }
    mock_response.status_code = 200
    mock_secops_client.rules.session.request.return_value = mock_response

    rules_resp = mock_secops_client.rules.list_rules()
    assert isinstance(rules_resp, RuleList)
    assert len(rules_resp.rules) == 1
    assert rules_resp.rules[0].display_name == "test_rule"
    assert rules_resp.next_page_token == "token_123"


def test_secops_get_rule_deployment(mock_secops_client):
    # Mock Response for RuleDeployment
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "name": "projects/123/locations/us/instances/abc/rules/rule_1/deployment",
        "enabled": True,
        "alerting": False,
        "runFrequency": "LIVE"
    }
    mock_response.status_code = 200
    mock_secops_client.rules.session.request.return_value = mock_response

    deployment = mock_secops_client.rules.get_rule_deployment("rule_1")
    assert isinstance(deployment, RuleDeployment)
    assert deployment.enabled is True
    assert deployment.alerting is False
    assert deployment.run_frequency == "LIVE"


def test_secops_get_rule(mock_secops_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "name": "projects/123/locations/us/instances/abc/rules/rule_1",
        "displayName": "test_rule",
        "text": "rule test_rule { condition: true }"
    }
    mock_response.status_code = 200
    mock_secops_client.rules.session.request.return_value = mock_response

    rule = mock_secops_client.rules.get_rule("rule_1")
    assert rule.display_name == "test_rule"
    assert "condition: true" in rule.text
