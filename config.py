import logging
import os

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = 'Text'  # Errbot will start in text mode (console only mode) and will answer commands from there.

BOT_DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/data"
BOT_EXTRA_PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__)) + "/plugins"
BOT_LOG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/logs/err.log"
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = ('@CHANGE_ME', )  # !! Don't leave that to "@CHANGE_ME" if you connect your errbot to a chat system !!

# GITHUB_USERNAME = "username"

# The password can be the account's password or a personal access token created
# at https://github.com/settings/tokens
# TODO: Add support for two factor authentication by passing the "x-github-otp"
#       header.
#       See: https://developer.github.com/v3/auth/#working-with-two-factor-authentication
# GITHUB_PASSWORD = "token"

GITHUB_PR_TEMPLATE = "{pr} | {status}, created {created_at} by {user}: {title} {labels} {assignee}"
# GITHUB_ISSUE_TEMPLATE = "{issue} | {status}, created {created_at} by {user}: {title} {labels} {assignee}"
