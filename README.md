# linkbot

Uses the [Errbot](https://errbot.readthedocs.io/en/latest/index.html) python bot framework to expand links.

It's kind of like Slack when it expands links:

![slack-expand](https://raw.githubusercontent.com/dmsimard/linkbot/master/docs/images/slack-expand.png)

It is usable across the [different messaging backends](https://errbot.readthedocs.io/en/latest/features.html) (like IRC!) supported by Errbot.

# Setting up and running

```
git clone https://github.com/dmsimard/linkbot
cd linkbot
# Tweak config.py if need be
python3 -m venv /path/to/venv
/path/to/venv/bin/pip install -r requirements.txt
/path/to/venv/bin/errbot
```

## GitHub Links

The following settings must be set in ``config.py``:
- ``GITHUB_USERNAME``: your github username
- ``GITHUB_PASSWORD``: a github [token](https://github.com/settings/tokens)
- ``GITHUB_PR_TEMPLATE``: a f-string formatted template that will be used to expand the pr

When seeing a GitHub pull request link, linkbot will reply to the message based on the configured template, for example:

```
> contributor: anyone available to check this pr ? https://github.com/dmsimard/linkbot/pull/3
> linkbot: https://github.com/dmsimard/linkbot/pull/3 | open, created 2020-09-11T03:22:14Z by dmsimard: Add a new .meta file [documentation,enhancement,meta]
```
