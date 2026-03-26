import pytest
import os
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch
from secops_toolkit.cli.cli import main

@pytest.fixture
def cli_runner():
    return CliRunner()

def test_cli_secops_configure_prompts(cli_runner, tmp_path):
    """Verify that configure command correctly prompts and saves a profile."""
    # Mock home directory to avoid affecting actual user config
    mock_home = tmp_path / "home"
    mock_home.mkdir()
    
    with patch("pathlib.Path.home", return_value=mock_home), \
         patch("secops_toolkit.utils.config_manager.GLOBAL_CONFIG_DIR", mock_home / ".secops-toolkit"), \
         patch("secops_toolkit.utils.config_manager.PROFILES_DIR", mock_home / ".secops-toolkit" / "profiles"), \
         patch("secops_toolkit.utils.config_manager.ACTIVE_CONFIG_FILE", mock_home / ".secops-toolkit" / ".env"):
        
        # Input for: region, endpoint, project, instance
        result = cli_runner.invoke(main, ["secops", "configure", "--profile", "test_profile"], 
                                   input="us\nhttps://api.test\n12345\ninst-abc\n")
        
        assert result.exit_code == 0
        assert "Profile 'test_profile' successfully saved" in result.output
        
        profile_file = mock_home / ".secops-toolkit" / "profiles" / "test_profile.env"
        assert profile_file.exists()
        content = profile_file.read_text()
        assert "SECOPS_REGION=" in content
        assert "us" in content

def test_cli_secops_select_config(cli_runner, tmp_path):
    """Verify that select-config correctly activates a global profile."""
    mock_home = tmp_path / "home"
    mock_home.mkdir()
    
    with patch("pathlib.Path.home", return_value=mock_home), \
         patch("secops_toolkit.utils.config_manager.GLOBAL_CONFIG_DIR", mock_home / ".secops-toolkit"), \
         patch("secops_toolkit.utils.config_manager.PROFILES_DIR", mock_home / ".secops-toolkit" / "profiles"), \
         patch("secops_toolkit.utils.config_manager.ACTIVE_CONFIG_FILE", mock_home / ".secops-toolkit" / ".env"):

        # 1. Create a profile
        cli_runner.invoke(main, ["secops", "configure", "--profile", "test_prof"], 
                          input="us\nhttps://api.test\n12345\ninst-abc\n")
        
        # 2. Select it
        result = cli_runner.invoke(main, ["secops", "select-config", "--profile", "test_prof"])
        assert result.exit_code == 0
        assert "is now active globally" in result.output
        
        # 3. Check if .env is created or copied correctly
        active_env = mock_home / ".secops-toolkit" / ".env"
        assert active_env.exists()

def test_cli_secops_lazy_init(cli_runner):
    """Verify that the secops group allows subcommands even without environment variables."""
    # We clear the environment and ensure load_dotenv doesn't find any file
    with patch.dict(os.environ, {}, clear=True), \
         patch("secops_toolkit.clients.secops_feature_clients.base.load_dotenv"):
         
         # Running "configure --help" should NOT crash with RuntimeError
         result = cli_runner.invoke(main, ["secops", "configure", "--help"])
         assert result.exit_code == 0
         assert "Show this message and exit" in result.output
