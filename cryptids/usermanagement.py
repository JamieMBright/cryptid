"""Manage all the user stored settings."""
import json
import logging
import os
import sys

from cryptids.utils import check_type, clean_string
import cryptids.settings as get

FILEPATH = os.path.join(os.getcwd(), "users", "user_details.json")

logger = logging.getLogger(__name__)
if get.VERBOSE:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def load_all_users():
    """Load all the user data."""
    with open(FILEPATH, "r") as f:
        data = json.load(f)
    return data


def load_user(username: str = "default", password: str = "Password123!"):
    """
    Load a single user.

    Parameters
    ----------
        username : str,
            The user you wish to load. defailt is 'default'.

        password : str,
            The password to unlock this user info. default is 'Password123!'.

    Returns
    -------
        (exit_code, user) : Tuple[int, dict],
            The dictionary of the user.

            (0, user), successful authentication
            (1, str), unrecognised username
            (2, str), incorrect password

    """
    # checks
    check_type(username, "username", str)
    check_type(password, "password", str)

    # safety. Don't want to inadvertently process a passed string.
    stripped_username = clean_string(username)
    stripped_password = clean_string(password)

    # log
    logger.info(f"checking user: '{stripped_username}' and password: '{stripped_password}'.")

    # load all the users
    all_users = load_all_users()

    # check if the user exists
    if username not in all_users.keys():
        logger.error(f"user '{stripped_username}' not in list.")
        return (1, "Unrecognised username")

    # if not, then load user
    user = all_users[stripped_username]

    # check the credentials
    if user["password"] != stripped_password:
        return (2, "Incorrect password")

    return (0, user)


def get_setting(user: dict, setting: str):
    """Getter for user settings."""
    # checks
    check_type(user, "user", dict)
    check_type(setting, "setting", str)
    if setting not in user.keys():
        return None
    elif setting == "password":
        return None
    else:
        return user[setting]


def set_setting(username: str, user: dict, setting: str, new_value):
    """Setter for user setting."""
    # checks
    check_type(username, "usenamer", str)
    check_type(user, "user", dict)
    check_type(setting, "setting", str)

    # get all the information
    data = load_all_users()

    # check if the user exists
    stripped_username = clean_string(username)
    if stripped_username not in data.keys():
        logger.error(f"user '{stripped_username}' not in list.")
        raise ValueError(f"Unrecognised username: {stripped_username}")

    # replace the settings
    data[stripped_username][setting] = new_value

    # Save the modified data back to the JSON file
    with open(FILEPATH, "w") as f:
        json.dump(data, f)
