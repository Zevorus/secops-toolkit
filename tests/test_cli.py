import pytest
import json
from click.testing import CliRunner
from unittest.mock import MagicMock, patch
from secops_toolkit.cli.cli import main
from secops_toolkit.model.secops.rules_model import RuleList, Rule, RuleDeployment
from secops_toolkit.model.secops.rules_model import RunFrequency


@pytest.fixture
def cli_runner():
    return CliRunner()


def test_cli_secops_rules_list(cli_runner):
    with patch("secops_toolkit.cli.secops.cli_secops.SecOpsClient") as mock_client:
        rule_id = "ru_123"
        instance = mock_client.return_value
        instance.rules.list_rules.return_value = RuleList(
            rules=[Rule(name=f"projects/123/locations/us/instances/abc/rules/{rule_id}", displayName="Test Rule")],
            next_page_token=""
        )

        # Test listing with default (only ID)
        result = cli_runner.invoke(main, ["secops", "rules", "list"])
        assert result.exit_code == 0
        assert rule_id in result.output

        # Test listing with table
        result = cli_runner.invoke(main, ["secops", "rules", "list", "--table"])
        assert result.exit_code == 0
        assert "RULE NAME" in result.output
        assert "Test Rule" in result.output


def test_cli_secops_rules_get_deployment(cli_runner):
    with patch("secops_toolkit.cli.secops.cli_secops.SecOpsClient") as mock_client:
        rule_id = "ru_123"
        instance = mock_client.return_value
        instance.rules.get_rule_deployment.return_value = RuleDeployment(
            name=f"projects/123/locations/us/instances/abc/rules/{rule_id}/deployment",
            enabled=True,
            alerting=True,
            run_frequency=RunFrequency.LIVE
        )

        result = cli_runner.invoke(main, ["secops", "rules", "get-deployment", rule_id])
        assert result.exit_code == 0
        assert '"enabled": true' in result.output
        assert '"runFrequency": "LIVE"' in result.output