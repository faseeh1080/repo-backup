from common import *


def update_repos(repo_paths):
    total_no_of_repos = len(repo_paths)

    for i in range(total_no_of_repos):
        rprint(f"Updating repo {i+1} / {total_no_of_repos}: {repo_paths[i]}")
        execute("git", "fetch", "--verbose", "origin", cwd=repo_paths[i])

    print(f"\033[KAll repositories have been updated.")


def update_lfs_files(repo_paths):
    total_no_of_repos = len(repo_paths)

    for i in range(total_no_of_repos):
        rprint(
            f"Fetching LFS files for repo {i+1} / {total_no_of_repos}: {repo_paths[i]}"
        )
        execute("git", "lfs", "fetch", "--all", cwd=repo_paths[i])

    print("\033[KAll LFS files have been fetched.")
