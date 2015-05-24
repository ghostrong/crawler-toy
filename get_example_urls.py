#coding=utf8

import urllib2
from lxml import etree

PARSER = etree.HTMLParser()

book_url = 'http://book.douban.com/latest?icn=index-latestbook-all'
text = urllib2.urlopen(book_url).read()

tree = etree.fromstring(text, PARSER)

output = 'urls.txt'
with open(output, 'w') as f:
    link_list = tree.xpath('//div[@class="article"]/ul/li/a[@href]')
    for link in link_list:
        url = link.get('href')
        f.write('%s\n' % url)

    link_list = tree.xpath('//div[@class="aside"]/ul/li/a[@href]')
    for link in link_list:
        url = link.get('href')
        f.write('%s\n' % url)
