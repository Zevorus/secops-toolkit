import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock
from unittest.mock import patch
from secops_toolkit.cli.cli import main

@pytest.fixture
def cli_runner():
    return CliRunner()

def test_cli_secops_rules_list(cli_runner):
    with patch("secops_toolkit.cli.secops.rules.cli_secops_rules.SecOpsClient") as mock_client:
        instance = mock_client.return_value
        instance.rules.list_rules.return_value = {"ruleDeployments": []}

        result = cli_runner.invoke(main, ["secops", "rules", "list-custom-rules"])

        assert result.exit_code == 0