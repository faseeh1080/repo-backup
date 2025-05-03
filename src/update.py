from common import *
import click


def update_repos(repo_paths):
    total_no_of_repos = len(repo_paths)

    for i in range(total_no_of_repos):
        click.echo(
            f"\033[KUpdating repo {i+1} / {total_no_of_repos}: {repo_paths[i]}\r",
            nl=False,
        )
        execute("git", "fetch", "--verbose", "origin", cwd=repo_paths[i])

    click.echo(f"\033[KAll repositories have been updated.")


def update_lfs_files(repo_paths):
    total_no_of_repos = len(repo_paths)

    for i in range(total_no_of_repos):
        click.echo(
            f"\033[KFetching LFS files for repo {i+1} / {total_no_of_repos}: {repo_paths[i]}\r",
            nl=False,
        )
        execute("git", "lfs", "fetch", "--all", cwd=repo_paths[i])

    click.echo("\033[KAll LFS files have been fetched.")
