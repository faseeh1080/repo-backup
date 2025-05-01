import os
import sys
import click

from common import *
from clone import clone_repos
from update import *
from config import get_config

BACKUP_DIR = "backup"


def check_git():
    if os.system("git --version") != 0:
        print(
            "Oops! Looks like Git is not installed or added to your PATH. Please rerun the program after fixing the issue."
        )
        sys.exit(1)


@click.group()
def cli():
    pass


@click.command(help="Backs up your repositories according to `config.json`")
def backup():
    config = get_config()

    check_git()

    os.makedirs(BACKUP_DIR, exist_ok=True)
    clone_repos(config, BACKUP_DIR)

    repo_paths = [os.path.join(BACKUP_DIR, repo) for repo in os.listdir(BACKUP_DIR)]

    update_repos(repo_paths)

    if config["lfs"]:
        update_lfs_files(repo_paths)

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
