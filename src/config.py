import json

from common import *


def configure():
    print("\nWelcome! Lets configure your backup program. You only need to do it once.")

    config = {"users-and-organizations": [], "other-repos": [], "lfs": False}

    print(
        "Enter the GitHub users and organizations whose repositories you want to clone, one by one. All of their public repositories will be cloned. Press Enter when you're done."
    )
    config["users-and-organizations"].extend(get_list_input())

    print(
        "Enter the web URLs of other repositories one by one. Press Enter when you are done."
    )
    config["other-repos"].extend(get_list_input())

    config["lfs"] = ask_yes_or_no(
        "Do you want to backup your LFS files? If you have Git LFS installed, I recommend turning this on."
    )

    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

    print("Configuration complete! Program will start shortly.\n")
    return config
