import sys
import os
import json
import click


def get_config():
    if not os.path.exists("config.json"):
        config = {
            "users-and-organizations": [],
            "ignored-repos": [],
            "other-repos": [],
            "lfs": False,
            "backup-directory": "backup",
        }

        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)

        click.echo(
            "`config.json` has been generated. Check the README to know how to configure the program."
        )
        sys.exit()

    else:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)

    if len(config["users-and-organizations"]) == 0 and len(config["other-repos"]) == 0:
        click.echo(
            "`config.json` looks empty. Please fill in some information. Check the README to learn more."
        )
        sys.exit(1)

    return config
