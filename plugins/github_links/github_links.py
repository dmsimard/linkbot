from errbot import BotPlugin

import re
from urllib.parse import urlparse
import requests


class GithubLinks(BotPlugin):
    def activate(self):
        """
        Triggers on plugin activation
        """
        super(GithubLinks, self).activate()
        configs = ["GITHUB_USERNAME", "GITHUB_PASSWORD", "GITHUB_PR_TEMPLATE"]
        for key in configs:
            if not hasattr(self.bot_config, key):
                raise Exception(f"{key} must be set in config.py")

        # Set up a session for authenticating with token
        self.session = requests.Session()
        self.session.auth = (self.bot_config.GITHUB_USERNAME, self.bot_config.GITHUB_PASSWORD)
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.nightshade-preview+json"
        })

        # To keep track of expanded links so we don't expand the same links too often
        self.expanded_links = []

    def callback_message(self, mess):
        """
        Triggered for every received message that isn't coming from the bot itself
        """
        try:
            url = re.search("(?P<url>https?://[^\s]+)", mess.body).group("url")
        except AttributeError:
            # There's no https URL in the message, nothing else to do here
            return False

        parsed_url = urlparse(url)
        if parsed_url.netloc != "github.com":
            # We're only interested in github.com links
            return False

        match_pr = re.search("/pull/\d+", parsed_url.path)
        if match_pr:
            try:
                self.send(mess.to, self.expand_pr(url))
                return True
            except Exception as e:
                print(f"expand_pr exception: {str(e)}")
                return False

        # TODO
        """
        match_issues = re.search("/issues/\d+", parsed_url.path)
        if match_issues:
            try:
                self.send(mess.frm, self.expand_issue(url))
            except Exception as e:
                print(f"expand_issue exception: {str(e)}")
                return False
        """

    def expand_pr(self, link):
        if link in self.expanded_links:
            return
        else:
            self.expanded_links.append(link)

        # Only keep the last 5 expanded links
        self.expanded_links = self.expanded_links[-5:]

        # Parse an url like https://github.com/ansible-collections/community.general/pull/786
        url = urlparse(link)
        namespace, repo, pull, pull_id = url.path[1:].split("/")

        # Craft the url we need to query this pull request
        # https://developer.github.com/v3/pulls/#get-a-pull-request
        endpoint = f"https://api.github.com/repos/{namespace}/{repo}/pulls/{pull_id}"

        # Get PR details and parse what we need from the API
        pr_details = self.session.get(endpoint).json()

        labels = [label["name"] for label in pr_details["labels"]]
        assignee = pr_details["assignee"]

        return self.bot_config.GITHUB_PR_TEMPLATE.format(
            pr=link,
            status=pr_details["state"],
            created_at=pr_details["created_at"],
            title=pr_details["title"],
            user=pr_details["user"]["login"],
            labels=f"[{','.join(labels)}]" if labels else "",
            assignee=f"(assigned to {assignee})" if assignee is not None else ""
        )
