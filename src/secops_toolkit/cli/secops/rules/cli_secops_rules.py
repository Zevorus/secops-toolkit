import click
import json
from typing import List, Optional
from secops_toolkit.clients.secops_client import SecOpsClient
from secops_toolkit.cli.utils.parse_rule_name import parse_rule_name
from secops_toolkit.model.secops.rules_model import Rule


def _format_rules_output(rules: List[Rule], table: bool, show_name: bool):
    """Internal helper to standardize rule formatting."""
    if not rules:
        click.echo("No rules found or error occurred.")
        return

    if table:
        click.echo(f"{'RULE NAME':<60} | {'RULE ID'}")
        click.echo("-" * 100)
        for rule in rules:
            parsed = parse_rule_name(rule.name)
            display_name = rule.display_name or "N/A"
            click.echo(f"{display_name:<60} | {parsed.rule_id}")
    else:
        for rule in rules:
            if show_name:
                click.echo(rule.display_name or "N/A")
            else:
                parsed = parse_rule_name(rule.name)
                click.echo(parsed.rule_id)


@click.group()
def rules():
    """Commands for Google SecOps YARA-L Detection Rules"""
    pass


@rules.command(name="list")
@click.pass_obj
@click.option("--page-size", default=10, help="Number of rules to list.", show_default=True)
@click.option("-t", "--table", is_flag=True, default=False, help="Display Name and ID in a table.")
@click.option("-N", "--show-name", is_flag=True, default=False, help="Show Display Name instead of Rule ID.")
def list_rules(client: SecOpsClient, page_size: int, table: bool, show_name: bool):
    """List custom detection rules in the SecOps instance."""
    rules_resp = client.rules.list_rules(page_size=page_size)
    _format_rules_output(rules_resp.rules, table, show_name)


@rules.command(name="list-all")
@click.pass_obj
@click.option("-t", "--table", is_flag=True, default=False, help="Display Name and ID in a table.")
@click.option("-N", "--show-name", is_flag=True, default=False, help="Show Display Name instead of Rule ID.")
def list_all_rules(client: SecOpsClient, table: bool, show_name: bool):
    """List all custom detection rules (automatically handles all pages)."""
    rules = list(client.rules.list_all_rules())
    _format_rules_output(rules, table, show_name)


@rules.command(name="get-rule")
@click.argument("rule_id")
@click.option("-o", "--output", help="Output file path (defaults to {rule_id}.yaral).")
@click.pass_obj
def get_rule_command(client: SecOpsClient, rule_id: str, output: Optional[str]):
    """Fetch the raw YARA-L content of a rule and save it to a local file."""
    if not output:
        output = f"{rule_id}.yaral"

    click.echo(f"Fetching rule '{rule_id}'...")
    rule = client.rules.get_rule(rule_id=rule_id)
    if not rule:
        click.echo(f"Error: Rule '{rule_id}' not found.")
        return

    if not rule.text:
        click.echo(f"Error: Rule '{rule_id}' has no YARA-L text content.")
        return

    try:
        with open(output, "w") as f:
            f.write(rule.text)
        click.secho(f"Successfully saved YARA-L content to: {output}", fg="green")
    except Exception as e:
        click.echo(f"Error writing to file: {e}")


@rules.command(name="get-deployment")
@click.argument("rule_id")
@click.pass_obj
def get_deployment(client: SecOpsClient, rule_id: str):
    """View the operational status (deployment) of a specific rule."""
    deployment = client.rules.get_rule_deployment(rule_id=rule_id)
    if deployment:
        click.echo(json.dumps(deployment.model_dump(by_alias=True), indent=2))
    else:
        click.echo(f"Error: Rule '{rule_id}' deployment information could not be found.")
