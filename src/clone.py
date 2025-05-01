import requests
import os

from common import *


def generate_repo_name_from_url(url):
    return url[19:-4].replace("/", "-")


def get_public_repos(username):
    while True:
        response = requests.get(f"https://api.github.com/users/{username}/repos")

        if response.status_code == 200:
            break
        else:
            retry = ask_yes_or_no(
                f"Oops! Failed to fetch repositories (status code: {response.status_code}) due to a faulty network connection or an incorrect username. Do you want to try again?"
            )
            if not retry:
                return []

    response = response.json()
    repos = [repo["html_url"] + ".git" for repo in response]
    return repos


def clone_repos(config, destination):
    """Clones repos which are not cloned yet."""

    public_repos = []
    for usr_or_org in config["users-and-organizations"]:
        public_repos.extend(get_public_repos(usr_or_org))

    repos_to_clone = public_repos + config["other-repos"]

    cloned_repos = os.listdir(destination)
    repos_to_clone = [
        repo
        for repo in repos_to_clone
        if generate_repo_name_from_url(repo) not in cloned_repos
        and repo not in config["ignored-repos"]
    ]

    no_of_repos_to_clone = len(repos_to_clone)

    if no_of_repos_to_clone == 1:
        print("Found one repository that has not been cloned.")
    else:
        print(f"Found {no_of_repos_to_clone} repositories that have not been cloned.")

    no_of_repos_cloned = 0
    for repo in repos_to_clone:
        rprint(
            f"Cloning repo {no_of_repos_cloned + 1} / {no_of_repos_to_clone}: {repo}"
        )
        execute(
            "git",
            "clone",
            "--no-checkout",
            repo,
            os.path.join(destination, generate_repo_name_from_url(repo)),
        )
        no_of_repos_cloned += 1

    if no_of_repos_cloned:
        print(
            f"\033[KCloned {no_of_repos_cloned} {'repositories' if no_of_repos_cloned != 1 else 'repository'}"
        )
