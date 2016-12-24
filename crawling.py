# -*- coding: utf-8 -*-
from __future__ import print_function
from lxml import html
import csv
import time
import os
import redis
import requests

#This is just a comment!
titles = []
links = []
authors = []
authors_links = []
infos = []

redis_cache = redis.StrictRedis(host='localhost')


def get_from_cache(link):
    if redis_cache.get(link):
        response = redis_cache.get(link)

        return response

    else:
        response = requests.get(link).content
        redis_cache.set(link, response, ex=3600)

        return response


def socrates_scraper(code):
    global infos, titles, authors, links, authors_links

    source_code = html.fromstring(code)

    titles += [title.encode('utf-8') for title in
               source_code.xpath('//h2/a/text()')]

    authors += [author.encode('utf-8')
                for author in source_code.xpath(
            '//div[@class=\'entry-author\']/a/text()')]

    infos += [info.encode('utf-8') for info in
              source_code.xpath('//div[@class=\'entry-spot\']/text()') if
              info != '\r\n\t\t']
    infos = [a for a in infos if a != '\r\n']

    links += [link.encode('utf-8') for link in
              source_code.xpath('//h2/a/@href')]

    authors_links += [author_link.encode('utf-8') for author_link in
                      source_code.xpath(
                          '//div[@class=\'entry-author\']/a/@href')]


def csv_writer(filepath):
    new_file_name = os.path.join(os.getcwd(),
                                 filepath)
    rows = zip(titles, authors, infos, links, authors_links)
    with open(new_file_name, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Title', 'Author', 'Info', 'Link', 'Author Link'])
        for row in rows:
            writer.writerow(row)

page_count = 51
for i in xrange(1, page_count + 1):
    link = 'http://www.socratesdergi.com/2016/page/{}'.format(i)
    code = get_from_cache(link)
    print(i)

    socrates_scraper(code)
    # time.sleep(1)

infos = [info.strip('\n\t\t\t') for info in infos]
csv_writer('2016.csv')

titles = []; links = []; authors = []; authors_links = []; infos = []


page_count = 54
for i in xrange(1, page_count + 1):
    link = 'http://www.socratesdergi.com/2015/page/{}'.format(i)
    code = get_from_cache(link)
    print(i)

    socrates_scraper(code)
    # time.sleep(1)

infos = [info.strip('\n\t\t\t') for info in infos]
csv_writer('2015.csv')



