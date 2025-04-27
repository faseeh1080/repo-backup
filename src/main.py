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


def update_repos():
    for repo in os.listdir(BACKUP_DIR):
        os.system(f"cd {os.path.join(BACKUP_DIR, repo)} && git fetch origin")
        print(f"Updated {repo}")


if __name__ == "__main__":
    configuration = get_configuration()
    os.makedirs(BACKUP_DIR, exist_ok=True)
    clone_repos(configuration["repos"])
    update_repos()

    print("Your backup has been successfully completed.")
