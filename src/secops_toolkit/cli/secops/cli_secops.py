import click
import json
from secops_toolkit.clients.secops_client import SecOpsClient
from secops_toolkit.cli.secops.rules.cli_secops_rules import rules

@click.group()
@click.pass_context
def secops(context):
    """Commands for Google SecOps."""
    context.obj = SecOpsClient()
    pass

@secops.command()
@click.pass_obj
def test_connectivity(client: SecOpsClient):
    """Test connectivity to Google SecOps API."""
    if client.test_connectivity():
        click.echo("Successfully connected to Google SecOps Instance.")
    else:
        click.echo("Failed to connect to Google SecOps Instance.")

secops.add_command(rules)

@secops.command()
@click.pass_obj
def show_secops_api_endpoint(client: SecOpsClient):
    secops_api_endpoint = client.show_secops_api_endpoint()
    click.echo(secops_api_endpoint)