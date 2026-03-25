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
@click.option("--version", default="v1beta", help="API version to use.")
def test_connectivity(client: SecOpsClient, version):
    """Test connectivity to Google SecOps API."""
    client.set_version(version)
    if client.test_connectivity():
        click.echo("Successfully connected to Google SecOps Instance.")
    else:
        click.echo("Failed to connect to Google SecOps Instance.")

secops.add_command(rules)