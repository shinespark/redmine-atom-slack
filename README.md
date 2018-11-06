# Redmine_Slacker
Post to Slack from redmine's atom feed.

This scripts use `Slack Web API token` .  
Get Slack Web API token: [Legacy tokens | Slack](https://api.slack.com/custom-integrations/legacy-tokens)

# Usage

```
$ pipenv install
$ cp conf{_original,}.yml
$ vi conf.yml
$ crontab -e
# add <as you like time> pipenv run python <abs_path>/main.py
```

