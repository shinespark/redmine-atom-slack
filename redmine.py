#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


class Redmine(object):
    def __init__(self, atom_url: str):
        self.atom = requests.get(atom_url).text
        self.soup = BeautifulSoup(self.atom, 'lxml')
        self.updated_at = self.soup.find('feed').find('updated').string

    def get_new_entries(self, last_atom_updated_at: str):
        raw_entries = self.soup.find('feed').find_all('entry')
        new_entries = []

        for raw_entry in raw_entries:
            if raw_entry.find('updated').string > last_atom_updated_at:
                new_entry = {
                    'author_name': raw_entry.find('author').find('name').string,
                    'title': raw_entry.find('title').string,
                    'title_link': raw_entry.find('id').string,
                    'text': BeautifulSoup(raw_entry.find('content').string, 'lxml').get_text(),
                }
                new_entries.append(new_entry)
        return new_entries
