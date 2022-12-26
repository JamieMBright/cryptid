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


def get_setting(user: dict,
                setting_depth1: str,
                setting_depth2: str = None,
                setting_depth3: str = None):
    """Getter for user settings."""
    # checks
    check_type(user, "user", dict)
    check_type(setting_depth1, "setting", str)
    if setting_depth2 is not None:
        check_type(setting_depth2, "setting_depth2", str)
    if setting_depth3 is not None:
        check_type(setting_depth3, "setting_depth3", str)

    # prevent protected settings
    if setting_depth1 not in user.keys():
        out = None
    # get the unprotected setting
    else:
        # get the root setting
        depth1 = user[setting_depth1]
        # if we are not asking for deeper...
        if setting_depth2 is None:
            # then return this depth
            out = depth1
        else:
            # else we are looking for deeper. Check that the new depth exists
            if setting_depth2 not in depth1.keys():
                # if not, return None as a sign of missing variable.
                out = None
            else:
                # else the variable exists, extract this second tier
                depth2 = depth1[setting_depth2]
                # if we are looking for a third depth
                if setting_depth3 is None:
                    # otherwise return the depth 2
                    out = depth2
                else:
                    # else check that the setting exists,
                    if setting_depth3 not in depth2.keys():
                        # if it doesn't, return None to indicate failure.
                        out = None
                    else:
                        # else, return the third depth.
                        out = depth2[setting_depth3]

    return out


def set_setting(username: str,
                new_value,
                setting_depth1: str,
                setting_depth2: str = None,
                setting_depth3: str = None,
                force_new_user: bool = False):
    """Setter for user setting."""
    # checks
    check_type(username, "usename", str)
    check_type(setting_depth1, "setting_depth1", str)
    if setting_depth2 is not None:
        check_type(setting_depth2, "setting_depth2", str)

    # get all the information
    data = load_all_users()

    # check if the user exists
    stripped_username = clean_string(username)
    if not force_new_user:
        if stripped_username not in data.keys():
            logger.error(f"user '{stripped_username}' not in list.")
            raise ValueError(f"Unrecognised username: {stripped_username}")

    # replace the settings
    if setting_depth2 is None:
        data[stripped_username][setting_depth1] = new_value
    elif setting_depth3 is None:
        data[stripped_username][setting_depth1][setting_depth2] = new_value
    else:
        data[stripped_username][setting_depth1][setting_depth2][setting_depth3] = new_value

    # Save the modified data back to the JSON file
    with open(FILEPATH, "w") as f:
        json.dump(data, f)


def check_user_exists(username):
    """Check whether a user already exists."""
    users = load_all_users()
    return username in users.keys()


def make_new_user(username, password, email):
    """Make a new user."""
    if not check_user_exists(username):
        # make user
        set_setting(username, email, "email", force_new_user=True)
        set_setting(username, password, "password")
        set_setting(username, "[-1]", "settings", "nfts")
        set_setting(username, "[0]", "settings", "loadouts", "default")
        set_setting(username, 0, "records", "wins")
        set_setting(username, 0, "records", "losses")
        return (0, "user created")
    else:
        return (1, "user already exists")


def update_nfts(username):
    """
    Get the nfts for an associated web3 wallet.

    This should connect to a web3 and return the ids of all crytids nfts.
    """
    # !!! connect to web3
    # Get NFTS
    nfts_from_web3 = [0]
    # update the user
    set_setting(username, nfts_from_web3, "settings", "nfts")


class User(object):
    """
    Define a user account.

    The user MUST already exist. This is only used once the credentials have
    successfully passed.
    """

    def __init__(self, username: str, user: dict):
        logger.info(f"Making User class for {username}.")
        if not check_user_exists(username):
            logger.fatal(f"Should not be able to make a User object for a non existent user: {username}.")
            raise ValueError("This function should not be hit for an unknocn user.")
        self.username = username

        # force web3 update before gameplay
        logger.info("Updating the NFTs for this user.")
        update_nfts(username)

        # get settings
        self.loadouts = get_setting(user, "settings", "loadouts")
        self.nfts = get_setting(user, "settings", "nfts")
