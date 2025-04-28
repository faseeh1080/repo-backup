import json
import os
import subprocess
import sys

from config import configure

BACKUP_DIR = "backup"


def rprint(statement):
    print("\033[K" + str(statement), end="\r", flush=True)


def execute(*commands, cwd=None):
    subprocess.run(
        commands,
        cwd=cwd,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )


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


def clone_repos(repos):
    """Clones repos which are not cloned yet."""

    cloned_repos = os.listdir(BACKUP_DIR)
    number_of_repos_cloned = 0

    for repo in repos:
        name = repo[19:-4].replace("/", "-")

        if name not in cloned_repos:
            rprint(f"Cloning repo no {number_of_repos_cloned + 1}: {repo}")
            execute(
                "git", "clone", "--no-checkout", repo, os.path.join(BACKUP_DIR, name)
            )
            number_of_repos_cloned += 1

    if number_of_repos_cloned:
        print(
            f"\033[KCloned {number_of_repos_cloned} {'repositories' if number_of_repos_cloned != 1 else 'repository'}"
        )


def update_repos(repo_paths):
    no_of_repos_updated = 0

    for path in repo_paths:
        rprint(f"Updating {path}")
        execute("git", "fetch", "--verbose", "origin", cwd=path)
        no_of_repos_updated += 1

    print(f"\033[KAll repositories have been updated.")


def update_lfs_files(repo_paths):
    for path in repo_paths:
        rprint(f"Fetching LFS files for {path}")
        execute("git", "lfs", "fetch", "--all", cwd=path)

    print("\033[KAll LFS files have been fetched.")


if __name__ == "__main__":
    configuration = get_configuration()

    check_git()

    os.makedirs(BACKUP_DIR, exist_ok=True)
    clone_repos(configuration["repos"])

    repo_paths = [os.path.join(BACKUP_DIR, repo) for repo in os.listdir(BACKUP_DIR)]

    update_repos(repo_paths)

    if configuration["lfs"]:
        update_lfs_files(repo_paths)

    print("Your repositories have been backed up successfully.")
