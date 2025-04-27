import json
import os
import sys
import requests


def get_public_repos(username):
    response = requests.get(f"https://api.github.com/users/{username}/repos")

    if response.status_code != 200:
        print(f"Failed to fetch repositories: {response.status_code}")
        return None

    response = response.json()
    repos = [repo["html_url"] + ".git" for repo in response]
    return repos


def get_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            return config

    print("Welcome! Lets configure your backup program. You only need to do it once.")

    config = {"username": "none", "repos": []}

    # Add username
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

    print("Configuration complete!\nYour repos will soon be cloned.")
    return config


def clone_repos(repos):
    """Clones repos which are not cloned yet."""
    result = os.system("git --version")
    if result != 0:
        print(
            "Oops! Looks like Git is not installed or added to your PATH. Please rerun the program after fixing the issue."
        )
        sys.exit()

    backup_dir = "backup"

    cloned_repos = os.listdir(backup_dir)

    for repo in repos:
        name = repo[19:-4].replace("/", "-")
        if name not in cloned_repos:
            os.system(f"git clone --no-checkout {repo} {backup_dir}/{name}")


if __name__ == "__main__":
    config = get_config()
    clone_repos(config["repos"])

    print("Your backup has been successfully completed.")
