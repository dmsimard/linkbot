# linkbot

Uses the [Errbot](https://errbot.readthedocs.io/en/latest/index.html) python bot framework to expand links.

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
> contributor: anyone available to check this pr ? https://github.com/namespace/repo/pull/12345
> linkbot: https://github.com/namespace/repo/pull/12345 | open, created 2020-05-18T14:34:02Z by contributor: New incredible feature [feature, core, WIP]
```
