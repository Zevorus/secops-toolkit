import click
import json
from secops_toolkit.clients.secops_client import SecOpsClient
from secops_toolkit.cli.secops.cli_secops import secops
from secops_toolkit.cli.gti.cli_gti import gti


@click.group()
def main():
    """Google Security Operations CLI toolkit."""
    pass

main.add_command(secops)
main.add_command(gti)

if __name__ == "__main__":
    main()
