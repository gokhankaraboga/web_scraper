# -*- coding: utf-8 -*-
from __future__ import print_function
from lxml import html
import csv
import os
import requests
import threading

titles = []
links = []
authors = []
authors_links = []
infos = []


def socrates_scraper(**kwargs):
    global infos, titles, authors, links, authors_links
    response = requests.get(kwargs['url'])
    source_code = html.fromstring(response.content)

    titles += [title.encode('utf-8') for title in
               source_code.xpath('//h2/a/text()')]

    authors += [author.encode('utf-8')
                for author in source_code.xpath(
            '//div[@class=\'entry-author\']/a/text()')]

    infos += [info.encode('utf-8') for info in
              source_code.xpath('//div[@class=\'entry-spot\']/text()') if
              info != '\r\n\t\t']

    links += [link.encode('utf-8') for link in
              source_code.xpath('//h2/a/@href')]

    authors_links += [author_link.encode('utf-8') for author_link in
                      source_code.xpath(
                          '//div[@class=\'entry-author\']/a/@href')]


page_count = 45
for i in xrange(1, page_count + 1):
    link = 'http://www.socratesdergi.com/kategori/yorum/page/{}'.format(i)
    url = {'url': link}

    t = threading.Thread(target=socrates_scraper, kwargs=url)
    t.start()
    t.join()

infos = [info.strip('\n\t\t\t') for info in infos]

new_file_name = os.path.join('/Users/gokhankaraboga/Desktop',
                             'socrates_yorum.csv')
rows = zip(titles, authors, infos, links, authors_links)
with open(new_file_name, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Title', 'Author', 'Info', 'Link', 'Author Link'])
    for row in rows:
        writer.writerow(row)

        # unicode(row).encode("utf-8")
