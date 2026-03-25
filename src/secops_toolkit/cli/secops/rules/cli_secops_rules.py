import click
import json
from secops_toolkit.clients.secops_client import SecOpsClient
from secops_toolkit.cli.utils.parse_rule_name import parse_rule_name


@click.group()
def rules():
    """Commands for Google SecOps YARA-L Detection Rules"""
    pass

@rules.command()
@click.pass_obj
@click.option("--page-size", default=10, help="Number of rules to list.", show_default=True)
def get_rules(client: SecOpsClient, page_size: int):
    """List custom detection rules in the SecOps instance."""
    rules = client.rules.list_rules(page_size=page_size)
    if len(rules.rules) > 0:
        for rule in rules.rules:
            parsed_rule_name = parse_rule_name(rule.name)
            click.echo(parsed_rule_name.rule_id )
    else:
        click.echo("No rules found or error occurred.")


@rules.command()
@click.pass_obj
def get_all_rules(client: SecOpsClient):
    """List all custom detection rules (automatically handles all pages)."""
    for rule in client.rules.list_all_rules():
        parsed = parse_rule_name(rule.name)
        click.echo(parsed.rule_id)

        
    
        

