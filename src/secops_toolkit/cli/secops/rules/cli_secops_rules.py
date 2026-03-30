import click
import json
import re
from typing import List, Optional
from datetime import datetime, timedelta, timezone
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


def _extract_rule_name(rule_text: str) -> Optional[str]:
    match = re.search(r"rule\s+([A-Za-z0-9_]+)\s*\{", rule_text)
    return match.group(1) if match else None


def _get_default_start_time() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=4, hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get_default_end_time() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")


@click.group()
def rules():
    """Commands for Google SecOps YARA-L Detection Rules"""
    pass


@rules.command(name="list")
@click.pass_obj
@click.option("--page-size", default=10, help="Number of rules to list.", show_default=True)
@click.option("-t", "--table", is_flag=True, default=False, help="Display Name and ID in a table.")
@click.option("-N", "--show-name", is_flag=True, default=False, help="Show Display Name instead of Rule ID.")
@click.option("--filter-name", help="Filter rules by display name (case-insensitive substring match).")
def list_rules(client: SecOpsClient, page_size: int, table: bool, show_name: bool, filter_name: Optional[str]):
    """List custom detection rules in the SecOps instance."""
    # If filter_name is provided, we must fall back to list_all to filter through them
    if filter_name:
        rules_list = list(client.rules.list_all_rules(name_filter=filter_name, limit=page_size))
        _format_rules_output(rules_list, table, show_name)
    else:
        rules_resp = client.rules.list_rules(page_size=page_size)
        _format_rules_output(rules_resp.rules, table, show_name)


@rules.command(name="list-all")
@click.pass_obj
@click.option("-t", "--table", is_flag=True, default=False, help="Display Name and ID in a table.")
@click.option("-N", "--show-name", is_flag=True, default=False, help="Show Display Name instead of Rule ID.")
@click.option("--filter-name", help="Filter rules by display name (case-insensitive substring match).")
@click.option("--limit", type=int, help="Maximum number of rules to return.")
def list_all_rules(client: SecOpsClient, table: bool, show_name: bool, filter_name: Optional[str], limit: Optional[int]):
    """List all custom detection rules (automatically handles pagination)."""
    rules_list = list(client.rules.list_all_rules(name_filter=filter_name, limit=limit))
    _format_rules_output(rules_list, table, show_name)


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
    if not rule or not rule.text:
        click.echo(f"Error: Rule '{rule_id}' not found or empty.")
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


@rules.command(name="verify")
@click.argument("file_path", type=click.Path(exists=True))
@click.pass_obj
def verify_rule(client: SecOpsClient, file_path: str):
    """Verifies a raw YARA-L file syntax via the v1alpha verifyRuleText API."""
    with open(file_path, "r") as f:
        text = f.read()

    click.echo(f"Verifying {file_path}...")
    resp = client.rules.verify_rule_text(text)
    if not resp:
        click.echo("Failed to get verification response.")
        return

    comp_state = resp.compilation_state or (resp.rule.compilation_state if resp.rule else None)
    diagnostics = resp.compilation_diagnostics or (resp.rule.compilation_diagnostics if resp.rule else [])

    if comp_state == "SUCCEEDED" or (comp_state is None and not diagnostics):
        click.secho("Verification SUCCEEDED.", fg="green")
    else:
        click.secho(f"Verification {comp_state}", fg="red")
        for diag in diagnostics:
            click.echo(f" - {diag.message}")


@rules.command(name="test")
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--start-time", help="Test start time (ISO 8601).", default=_get_default_start_time)
@click.option("--end-time", help="Test end time (ISO 8601).", default=_get_default_end_time)
@click.pass_obj
def test_rule(client: SecOpsClient, file_path: str, start_time: str, end_time: str):
    """Runs a legacy retro-hunt test on a local YARA-L file."""
    with open(file_path, "r") as f:
        text = f.read()

    click.echo(f"Running test for {file_path} from {start_time} to {end_time}...")
    result = client.rules.run_test_rule(text, start_time, end_time)
    if result is None:
        click.echo("Test failed to initiate.")
    else:
        click.echo("Test Result Component:")
        click.echo(json.dumps(result, indent=2))


@rules.command(name="push")
@click.argument("file_path", type=click.Path(exists=True))
@click.option("-f", "--force-update", is_flag=True, default=False, help="Force update if rule exists.")
@click.pass_obj
def push_rule(client: SecOpsClient, file_path: str, force_update: bool):
    """Pushes a local YARA-L file to Google SecOps (creates or updates)."""
    with open(file_path, "r") as f:
        text = f.read()

    display_name = _extract_rule_name(text)
    if not display_name:
        click.echo("Error: Could not extract rule name from the YARA-L file.")
        return

    click.echo(f"Looking up rule by display name: {display_name}")
    # Search if rule exists
    existing_rules = list(client.rules.list_all_rules(name_filter=display_name))
    matched_rule = None
    for r in existing_rules:
        if r.display_name == display_name:
            matched_rule = r
            break

    if matched_rule:
        parsed = parse_rule_name(matched_rule.name)
        rule_id = parsed.rule_id
        if not force_update:
            click.secho(f"Error: Rule '{display_name}' ({rule_id}) already exists. Use --force-update to update.", fg="red")
            return
        
        click.echo(f"Updating existing rule {rule_id}...")
        res = client.rules.update_rule(rule_id, text)
        if res:
            click.secho(f"Successfully updated rule {rule_id}.", fg="green")
        else:
            click.secho(f"Failed to update rule.", fg="red")

    else:
        click.echo("Rule not found. Creating new rule...")
        res = client.rules.create_rule(text)
        if res:
            new_id = parse_rule_name(res.name).rule_id
            click.secho(f"Successfully created rule {new_id}.", fg="green")
        else:
            click.secho("Failed to create rule.", fg="red")
