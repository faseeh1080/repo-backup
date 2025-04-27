import json
import os
import subprocess
import sys

from config import configure

BACKUP_DIR = "backup"


def get_configuration():
    if not os.path.exists("config.json"):
        configuration = configure()
    else:
        with open("config.json", "r") as config_file:
            configuration = json.load(config_file)

    return configuration


def clone_repos(repos):
    """Clones repos which are not cloned yet."""
    if os.system("git --version") != 0:
        print(
            "Oops! Looks like Git is not installed or added to your PATH. Please rerun the program after fixing the issue."
        )
        sys.exit(1)

    cloned_repos = os.listdir(BACKUP_DIR)

    for repo in repos:
        name = repo[19:-4].replace("/", "-")
        if name not in cloned_repos:
            print(f"\033[Kgit clone: {repo}", end="\r", flush=True)
            subprocess.run(
                ["git", "clone", "--no-checkout", repo, os.path.join(BACKUP_DIR, name)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
    print("\033[Kgit clone complete.")


def update_repos(repo_paths):
    for path in repo_paths:
        print(f"\033[Kgit fetch: {path}", end="\r", flush=True)
        subprocess.run(
            ["git", "fetch", "--verbose", "origin"],
            cwd=path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    print("\033[Kgit fetch complete.")


def update_lfs_files(repo_paths):
    for path in repo_paths:
        print(f"\033[Kgit lfs fetch: {path}", end="\r", flush=True)
        subprocess.run(
            ["git", "lfs", "fetch", "--all"],
            cwd=path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    print("\033[Kgit lfs fetch complete.")


if __name__ == "__main__":
    configuration = get_configuration()

    os.makedirs(BACKUP_DIR, exist_ok=True)
    clone_repos(configuration["repos"])

    repo_paths = [os.path.join(BACKUP_DIR, repo) for repo in os.listdir(BACKUP_DIR)]

    update_repos(repo_paths)

    if configuration["lfs"]:
        update_lfs_files(repo_paths)

    print("Your repositories have been backed up successfully.")
