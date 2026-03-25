import pytest
import json
from click.testing import CliRunner
from unittest.mock import MagicMock, patch
from secops_toolkit.cli.cli import main
from secops_toolkit.model.secops.rules_model import RuleList, Rule, RuleDeployment


@pytest.fixture
def cli_runner():
    return CliRunner()


def test_cli_secops_rules_list(cli_runner):
    with patch("secops_toolkit.cli.secops.cli_secops.SecOpsClient") as mock_client:
        instance = mock_client.return_value
        instance.rules.list_rules.return_value = RuleList(
            rules=[Rule(name="projects/123/locations/us/instances/abc/rules/rule_1", displayName="Test Rule")],
            next_page_token=""
        )

        # Test listing with default (only ID)
        result = cli_runner.invoke(main, ["secops", "rules", "list"])
        assert result.exit_code == 0
        assert "rule_1" in result.output

        # Test listing with table
        result = cli_runner.invoke(main, ["secops", "rules", "list", "--table"])
        assert result.exit_code == 0
        assert "RULE NAME" in result.output
        assert "Test Rule" in result.output


def test_cli_secops_rules_get_deployment(cli_runner):
    with patch("secops_toolkit.cli.secops.cli_secops.SecOpsClient") as mock_client:
        instance = mock_client.return_value
        instance.rules.get_rule_deployment.return_value = RuleDeployment(
            name="projects/123/locations/us/instances/abc/rules/rule_1/deployment",
            enabled=True,
            alerting=True,
            run_frequency="LIVE"  # note: the model uses run_frequency (alias: runFrequency)
        )

        result = cli_runner.invoke(main, ["secops", "rules", "get-deployment", "rule_1"])
        assert result.exit_code == 0
        assert '"enabled": true' in result.output
        assert '"runFrequency": "LIVE"' in result.output