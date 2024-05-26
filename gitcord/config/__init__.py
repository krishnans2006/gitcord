DEBUG = True

OWNER_ID = 731604933773885521
TEST_GUILDS = [1180270316799406211]

REMOTES_DEFAULTS = {
    "remote": "gh",
    "user": "krishnans2006",
    "repo": "dotfiles",
    "ref": None,
    "mr": None,
}


# Should be overwritten in secret.py
DISCORD_TOKEN = ""

try:
    from .secret import *
except ImportError:
    pass
