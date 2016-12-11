from lxml import html
import requests

titles = []
response = requests.get('http://www.socratesdergi.com/kategori/yorum/page/1')
source_code = html.fromstring(response.content)

while len(source_code.xpath('//div[@class=\'nav-previous\']/a/@href')) != 0:
    global titles
    link = source_code.xpath('//div[@class=\'nav-previous\']/a/@href')
    pass
    response = requests.get(link[0])
    source_code = html.fromstring(response.content)

    titles += [title.encode('utf-8') for title in
               source_code.xpath('//h2/a/text()')]

    pass
