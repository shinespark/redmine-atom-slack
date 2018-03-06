#!/usr/bin/env python
# coding: utf-8
from bs4 import BeautifulSoup
import json
import os
import urllib.parse
import urllib.request
import yaml

dirpath = os.path.abspath(os.path.dirname(__file__))
conf = yaml.load(open(dirpath + '/conf.yml').read())


def main():
    url = conf['atom_url']
    atom = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(atom, 'lxml')
    current_atom_updated_time = soup.find('feed').find('updated').string

    # get last_atom_updated_time
    try:
        f = open(dirpath + '/latest.txt', 'r')
        last_atom_updated_time = f.read().strip()
        f.close()
    except IOError:
        last_atom_updated_time = current_atom_updated_time

    entries = soup.find('feed').find_all('entry')
    for entry in entries:
        # skip old entry
        if entry.find('updated').string > last_atom_updated_time:
            continue

        if 'インシデント管理' not in entry.find('title').string:
            continue
        if '#change-' in entry.find('link')['href']:
            continue

        params = {
          'attachments': [
              {
                  'color': '#d11a1f',
                  'author_name': entry.find('author').find('name').string,
                  'title': entry.find('title').string,
                  'title_link': entry.find('id').string,
                  'text': BeautifulSoup(entry.find('content').string, 'lxml').get_text(),
                  'footer': 'Redmine-Slacker'
              }
          ],
          'channel': conf['channel'],
        }
        json_params = json.dumps(params).encode('utf-8')
        slack_url = conf['webhook_url']
        req = urllib.request.Request(slack_url, json_params, {'Content-type': 'application/json'})
        urllib.request.urlopen(req)

    # update latest_atom_update_time
    f = open(dirpath + '/latest.txt', 'w')
    f.write(current_atom_updated_time)
    f.close()


if __name__ == "__main__":
    main()
