#!/usr/bin/env python3
# TL;DR:
# Standalone CLI version of the Errbot plugin.
# translates https://github.com/<namespace>/<repo>/pull/<id> to:
# https://api.github.com/repos/<namespace>/<repo>/pulls/<id>
# query the endpoint and return a helpful message back

from urllib.parse import urlparse
import argparse
import requests
import os

TEMPLATE = "{pr} | Created {created_at} by {user}: {title} {labels}"

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", None)

# The password can be the account's password or a personal access token created
# at https://github.com/settings/tokens
# TODO: Add support for two factor authentication by passing the "x-github-otp"
#       header. See: https://developer.github.com/v3/auth/#working-with-two-factor-authentication
GITHUB_PASSWORD = os.environ.get("GITHUB_PASSWORD", None)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("pr", help="Link to the pull request")
    return parser.parse_args()


def main():
    args = get_args()

    if GITHUB_USERNAME is None or GITHUB_PASSWORD is None:
        raise Exception("Environment variables GITHUB_USERNAME and GITHUB_PASSWORD must be set.")

    # Parse an url like https://github.com/ansible-collections/community.general/pull/786
    url = urlparse(args.pr)
    namespace, repo, pull, pull_id = url.path[1:].split("/")

    # Craft the url we need to query this pull request
    # https://developer.github.com/v3/pulls/#get-a-pull-request
    endpoint = f"https://api.github.com/repos/{namespace}/{repo}/pulls/{pull_id}"

    # Set up a session for authenticating with token
    session = requests.Session()
    session.auth = (GITHUB_USERNAME, GITHUB_PASSWORD)
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.nightshade-preview+json"
    })

    # Get PR details and parse what we need from the API
    pr_details = session.get(endpoint).json()

    labels = [label["name"] for label in pr_details["labels"]]
    # It doesn't look like we use the "assignee" field in PRs very much
    # assignee = "(unassigned)"
    # if pr_details["assignee"] is not None:
    #     assignee = f"(assigned to {pr_details['assignee']})"

    msg = TEMPLATE.format(
        pr=args.pr,
        created_at=pr_details["created_at"],
        title=pr_details["title"],
        user=pr_details["user"]["login"],
        labels=f"[{','.join(labels)}]" if labels else ""
    )

    print(msg)

if __name__ == "__main__":
    main()

