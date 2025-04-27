import requests
import json


def ask_yes_or_no(question) -> bool:
    return input(question + " (y/N): ").strip().lower() == "y"


def get_public_repos(username):
    response = requests.get(f"https://api.github.com/users/{username}/repos")

    if response.status_code != 200:
        print(
            f"Failed to fetch repositories with status code {response.status_code}. Make sure you are connected to the internet."
        )
        return []

    response = response.json()
    repos = [repo["html_url"] + ".git" for repo in response]
    return repos


def configure():
    print("Welcome! Lets configure your backup program. You only need to do it once.")

    config = {"username": "name", "repos": [], "lfs": False}

    config["username"] = input("Enter your GitHub username: ")

    # Add all public repos
    if ask_yes_or_no(
        "Do you want to add all of your public repositories to the backup list?"
    ):
        print("Fetching your public repositories from GitHub.")
        config["repos"].extend(get_public_repos(config["username"]))

    # Add custom repos
    repo = "https://github.com/username/example.git"
    print(
        "Enter the web URLs of your other repositories one by one. Hit Enter when you are done."
    )
    while repo:
        repo = input(" > ").strip()
        if repo:
            config["repos"].append(repo)

    # LFS
    config["lfs"] = ask_yes_or_no(
        "Do you want to backup your LFS files? If you have Git LFS installed, I recommend turning this on."
    )

    # Store the configuration
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

    print("Configuration complete! Program will start shortly.\n")
    return config
