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


@click.command(help="Backs up your repositories according to `config.json`.")
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


cli.add_command(backup)

if __name__ == "__main__":
    cli()
