import json
import os
import sys
import requests


def get_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            return config

    config = {"username": "none"}
    config["username"] = input("Enter your GitHub username: ")

    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

    return config


def get_repos():
    response = requests.get(f"https://api.github.com/users/{config["username"]}/repos")

    if response.status_code != 200:
        print(f"Failed to fetch repositories: {response.status_code}")
        sys.exit()

    return response.json()


def clone_repos():
    result = os.system("git --version")
    if result != 0:
        print(
            "Please install Git or ensure it is added to the system PATH in order to clone repositories."
        )
        sys.exit()

    backup_dir = "backup"

    if os.path.exists(backup_dir):
        print(
            "A directory or file named `backup` already exists. Please ensure it is deleted or moved before rerunning the program."
        )
        sys.exit()

    for repo in repos:
        os.system(
            f"git clone --no-checkout https://github.com/{config["username"]}/{repo["name"]}.git {backup_dir}/{repo["name"]}"
        )


if __name__ == "__main__":
    config = get_config()
    repos = get_repos()
    clone_repos()

    print("Your backup has been successfully completed.")
