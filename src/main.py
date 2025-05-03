import os
import sys
import click

from common import *
from clone import clone_repos
from update import *
from config import get_config


@click.group()
def cli():
    pass


@click.command(help="Backs up your repositories according to `config.json`")
def backup():
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
        print("To also fetch LFS files, enable the option in `config.json`.")

    print("Your repositories have been backed up successfully.")


@click.command(help="Resets `config.json`")
def reset_config():
    config_file = "config.json"

    if os.path.exists(config_file):
        os.remove(config_file)

    get_config()


cli.add_command(backup)
cli.add_command(reset_config, name="reset")

if __name__ == "__main__":
    cli()
