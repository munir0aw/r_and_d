# Commands for r_and_d app
import click
from frappe.commands import pass_context, get_site

@click.command()
@pass_context
def r_and_d_command(context):
    """R&D App Command"""
    pass

commands = [
    r_and_d_command,
]
