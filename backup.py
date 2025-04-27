import json
import os
import sys
import requests

BACKUP_DIR = "backup"


def get_public_repos(username):
    response = requests.get(f"https://api.github.com/users/{username}/repos")

    if response.status_code != 200:
        print(f"Failed to fetch repositories: {response.status_code}")
        return None

    response = response.json()
    repos = [repo["html_url"] + ".git" for repo in response]
    return repos


def configure():
    print("Welcome! Lets configure your backup program. You only need to do it once.")

    config = {"username": "none", "repos": []}

    config["username"] = input("Enter your GitHub username: ")

    # Add all public repos
    if (
        input(
            "Do you want to add all of your public repositories to the backup list? (y/N): "
        )
        .strip()
        .lower()
        == "y"
    ):
        config["repos"].extend(get_public_repos(config["username"]))

    # Add custom repos
    repo = "https://github.com/username/example.git"
    print(
        "Enter the web URLs of other repositories one by one. Hit Enter when you are done."
    )
    while repo:
        repo = input(" > ").strip()
        if repo:
            config["repos"].append(repo)

    # Store the configuration
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

    print("Configuration complete!")
    return config


def get_config():
    if not os.path.exists("config.json"):
        config = configure()
    else:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)

    return config


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
    config = get_config()
    os.makedirs(BACKUP_DIR, exist_ok=True)
    clone_repos(config["repos"])
    update_repos()

    print("Your backup has been successfully completed.")
