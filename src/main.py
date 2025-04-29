import json
import os
import sys

from common import *
from config import configure
from clone import clone_repos

BACKUP_DIR = "backup"


def get_configuration():
    if not os.path.exists("config.json"):
        configuration = configure()
    else:
        with open("config.json", "r") as config_file:
            configuration = json.load(config_file)

    return configuration


def check_git():
    if os.system("git --version") != 0:
        print(
            "Oops! Looks like Git is not installed or added to your PATH. Please rerun the program after fixing the issue."
        )
        sys.exit(1)


def update_repos(repo_paths):
    total_no_of_repos = len(repo_paths)

    for i in range(total_no_of_repos):
        rprint(f"Updating repo {i+1} / {total_no_of_repos}: {repo_paths[i]}")
        execute("git", "fetch", "--verbose", "origin", cwd=repo_paths[i])

    print(f"\033[KAll repositories have been updated.")


def update_lfs_files(repo_paths):
    total_no_of_repos = len(repo_paths)

    for i in range(total_no_of_repos):
        rprint(
            f"Fetching LFS files for repo {i+1} / {total_no_of_repos}: {repo_paths[i]}"
        )
        execute("git", "lfs", "fetch", "--all", cwd=repo_paths[i])

    print("\033[KAll LFS files have been fetched.")


if __name__ == "__main__":
    configuration = get_configuration()

    check_git()

    os.makedirs(BACKUP_DIR, exist_ok=True)
    clone_repos(configuration, BACKUP_DIR)

    repo_paths = [os.path.join(BACKUP_DIR, repo) for repo in os.listdir(BACKUP_DIR)]

    update_repos(repo_paths)

    if configuration["lfs"]:
        update_lfs_files(repo_paths)

    print("Your repositories have been backed up successfully.")
