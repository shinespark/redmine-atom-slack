#!/usr/bin/env python
# coding: utf-8
import os
import yaml
from redmine import Redmine
from slack import Slack


def main(config_file_name: str):
    dirpath = os.path.abspath(os.path.dirname(__file__))
    conf = yaml.load(open(dirpath + '/' + config_file_name).read())
    r = Redmine(conf['atom_url'])

    try:
        f = open(dirpath + '/' + conf['last_updated_at'], 'r')
        last_updated_at = f.read().strip()
        f.close()
    except IOError:
        last_updated_at = r.updated_at

    entries = r.get_new_entries(last_updated_at)

    s = Slack(conf['webhook_url'], conf['channel'])

    for entry in entries:
        s.post(entry['author_name'], entry['title'], entry['title_link'], entry['text'])

    # update last_updated_at
    f = open(dirpath + '/' + conf['last_updated_at'], 'w')
    f.write(r.updated_at)
    f.close()


if __name__ == "__main__":
    main('conf.yml')
    main('conf_luna.yml')
