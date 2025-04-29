import subprocess


def rprint(statement):
    print("\033[K" + str(statement), end="\r", flush=True)


def execute(*commands, cwd=None):
    subprocess.run(
        commands,
        cwd=cwd,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
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
