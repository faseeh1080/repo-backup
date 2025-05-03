import subprocess
import sys
import os


def rprint(statement):
    print("\033[K" + str(statement), end="\r", flush=True)


def check_git():
    if os.system("git --version") != 0:
        print(
            "Oops! Looks like Git is not installed or added to your PATH. Please rerun the program after fixing the issue."
        )
        sys.exit(1)


def execute(*commands, cwd=None, verbose=False):
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

    print("\033[F\033[K", end="")
    return input_list
