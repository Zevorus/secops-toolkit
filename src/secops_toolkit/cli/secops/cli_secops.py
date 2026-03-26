import click
import json
from secops_toolkit.clients.secops_client import SecOpsClient
from secops_toolkit.cli.secops.rules.cli_secops_rules import rules
from secops_toolkit.utils.config_manager import (
    save_config,
    activate_profile,
    list_profiles,
)

@click.group()
@click.pass_context
def secops(context):
    """Commands for Google SecOps."""
    # Delay client initialization for config-related commands
    if (
        context.invoked_subcommand is not None
        and context.invoked_subcommand not in ["configure", "select-config"]
    ):
        try:
            context.obj = SecOpsClient()
        except RuntimeError:
            # Client initialization might fail if not configured
            pass

@secops.command()
@click.option("--profile", default="main_profile", help="Profile name to save to.")
def configure(profile):
    """Configure Google SecOps parameters for a specific profile."""
    click.echo(f"--- Configuring SecOps Profile: {profile} ---")

    region = click.prompt("Enter SECOPS_REGION (e.g., us)")
    endpoint = click.prompt("Enter SECOPS_API_ENDPOINT")
    project_number = click.prompt("Enter SECOPS_PROJECT_NUMBER")
    instance_id = click.prompt("Enter SECOPS_INSTANCE_ID")

    configs = {
        "SECOPS_REGION": region,
        "SECOPS_API_ENDPOINT": endpoint,
        "SECOPS_PROJECT_NUMBER": project_number,
        "SECOPS_INSTANCE_ID": instance_id,
    }

    try:
        path = save_config(configs, profile_name=profile)
        click.echo(f"\nProfile '{profile}' successfully saved to: {path}")
        click.echo(
            f"To use this profile, run: secops-toolkit secops select-config --profile {profile}"
        )
    except Exception as e:
        click.echo(f"\nError: {e}", err=True)

@secops.command("select-config")
@click.option("--profile", help="Profile name to activate.")
def select_config(profile):
    """Select the active profile to use for the toolkit."""
    profiles = list_profiles()

    if not profile:
        if not profiles:
            click.echo("No profiles found. Use 'secops-toolkit secops configure' first.")
            return

        click.echo("Available profiles:")
        for p in profiles:
            click.echo(f"  - {p}")

        profile = click.prompt("\nPlease enter the profile name to activate")

    if activate_profile(profile):
        click.echo(f"Success: Profile '{profile}' is now active globally.")
    else:
        click.echo(f"Error: Profile '{profile}' could not be found.", err=True)

@secops.command()
@click.pass_obj
def test_connectivity(client: SecOpsClient):
    """Test connectivity to Google SecOps API."""
    if client and client.test_connectivity():
        click.echo("Successfully connected to Google SecOps Instance.")
    else:
        click.echo("Failed to connect to Google SecOps Instance (check your configuration).")

secops.add_command(rules)

@secops.command()
@click.pass_obj
def show_secops_api_endpoint(client: SecOpsClient):
    """Show the currently configured API endpoint."""
    if client:
        secops_api_endpoint = client.show_secops_api_endpoint()
        click.echo(secops_api_endpoint)
    else:
        click.echo("Client not initialized. Check your configuration.")