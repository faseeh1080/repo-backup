import subprocess
import sys
import os
import click

verbose = False


def check_git():
    if os.system("git --version") != 0:
        click.echo(
            "Oops! Looks like Git is not installed or added to your PATH. Please rerun the program after fixing the issue."
        )
        sys.exit(1)


def execute(*commands, cwd=None):
    if verbose:
        click.echo("\033[K >>> " + " ".join(commands))

    subprocess.run(
        commands,
        cwd=cwd,
        check=True,
        stdout=None if verbose else subprocess.DEVNULL,
        stderr=None if verbose else subprocess.PIPE,
    )


def ask_yes_or_no(question) -> bool:
    return input(question + " (y/N): ").strip().lower() == "y"


def get_list_input() -> list:
    input_list = []
    inp = "example"
    while inp:
        inp = input(" > ").strip()
        if inp:
            input_list.append(inp)

    click.echo("\033[F\033[K", nl=False)
    return input_list
