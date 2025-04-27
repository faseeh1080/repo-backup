import json
import os
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
    result = os.system("git --version")
    if result != 0:
        print(
            "Oops! Looks like Git is not installed or added to your PATH. Please rerun the program after fixing the issue."
        )
        sys.exit()

    cloned_repos = os.listdir(BACKUP_DIR)

    for repo in repos:
        name = repo[19:-4].replace("/", "-")
        if name not in cloned_repos:
            os.system(f"git clone --no-checkout {repo} {BACKUP_DIR}/{name}")


def update_repos(repo_paths):
    for path in repo_paths:
        os.system(f"cd {path} && git fetch --verbose origin")


def update_lfs_files(repo_paths):
    if os.system("git lfs --version") != 0:
        print(
            "Oops! Looks like Git LFS is not installed. Please rerun the program after fixing the issue."
        )
        sys.exit()

    for path in repo_paths:
        os.system(f"cd {path} && git lfs fetch --all")


if __name__ == "__main__":
    configuration = get_configuration()
    os.makedirs(BACKUP_DIR, exist_ok=True)
    clone_repos(configuration["repos"])

    repo_paths = [os.path.join(BACKUP_DIR, repo) for repo in os.listdir(BACKUP_DIR)]
    update_repos(repo_paths)

    if configuration["lfs"]:
        update_lfs_files(repo_paths)

    print("Your backup has been successfully completed.")
