import requests
import json


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
