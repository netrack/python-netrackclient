from netrackclient.commands import ip

import os
import sys
import click


@click.command()
@click.option('-v', '--verbose', is_flag=True, help='enable verbose mode')
@context
def cli(context, verbose):
    pass
