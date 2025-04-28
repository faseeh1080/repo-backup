import requests
import json


def ask_yes_or_no(question) -> bool:
    return input(question + " (y/N): ").strip().lower() == "y"


def get_public_repos():
    username = input("Enter your GitHub username: ")

    while True:
        response = requests.get(f"https://api.github.com/users/{username}/repos")

        if response.status_code != 200:
            if ask_yes_or_no(
                f"Oops! Failed to fetch repositories (status code: {response.status_code}). Please verify your network connection and username. Would you like to skip this step?"
            ):
                return []
        else:
            break

    response = response.json()
    repos = [repo["html_url"] + ".git" for repo in response]
    return repos


def configure():
    print("\nWelcome! Lets configure your backup program. You only need to do it once.")

    config = {"repos": [], "lfs": False}

    # Add all public repos
    if ask_yes_or_no(
        "Do you want to add all of your public repositories to the backup list?"
    ):
        config["repos"].extend(get_public_repos())
        print("All of your public repositories have been added to the backup list.")

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
