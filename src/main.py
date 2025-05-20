# SPDX-License-Identifier: GPL-3.0

import os
import click

from common import *
from clone import clone_repos
from update import *
from config import get_config


@click.group()
def cli():
    pass


@click.command(help="Creates `config.json` file for configuration.")
def config():
    config_file = "config.json"

    if os.path.exists(config_file):
        os.remove(config_file)

    get_config()


@click.command(help="Backs up your repositories according to `config.json`")
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
def backup(verbose):
    import common

    common.verbose = verbose

    config = get_config()
    backup_dir = config["backup-directory"]

    check_git()

    os.makedirs(backup_dir, exist_ok=True)
    clone_repos(config, backup_dir)

    repo_paths = [os.path.join(backup_dir, repo) for repo in os.listdir(backup_dir)]

    update_repos(repo_paths)

    if config["lfs"]:
        update_lfs_files(repo_paths)
    else:
        click.echo("To fetch LFS files as well, enable the option in `config.json`.")

    click.echo("Your repositories have been backed up successfully.")


cli.add_command(config, name="config")
cli.add_command(backup)

if __name__ == "__main__":
    cli()
