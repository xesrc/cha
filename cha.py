#! /usr/bin/env python3

from sys import argv
from urllib import request
from lxml import etree
from optparse import OptionParser

headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}

def paserS(argv):
    url = "http://m.dict.cn/" + request.quote(argv)
    req = request.Request(url, headers=headers)
    page = request.urlopen(req).read()
    page = page.decode("utf-8")
    page = etree.HTML(page)
    words = page.xpath('//*[@id="sctlist"]/li[1]/div[1]/div/div/ul')
    meaning = page.xpath('//*[@id="sctlist"]/li[1]/div[1]/div/div/ul/li/strong')
    if len(meaning)>=1:
        print(meaning[0].text)
        phonetic = page.xpath('/html/body/div[1]/div/div[3]/span[1]/bdo')
        if len(phonetic)>=1:
            print('en:', phonetic[0].text)
        phonetic = page.xpath('/html/body/div[1]/div/div[3]/span[2]/bdo')
        if len(phonetic)>=1:
            print('us:', phonetic[0].text)
    else:
        if len(words)>=1:
            print("possible words are :")
            print("====================")
            for line in words[0]:
                print(line[0].text)
            print("====================")
def paserM(url):

    req = request.Request(url, headers=headers)
    page = request.urlopen(req).read()
    page = page.decode("utf-8")
    page = etree.HTML(page)
    meaning = page.xpath('//*[@id="sctlist"]/li[1]/div/div/div/ul/li/strong')
    if len(meaning)>=1:
        print(meaning[0].text)
def main():
    import os
    # command line options
    usage = '''eng-chs look up\n
usage:
\t%prog [options] <query> [query2 query3 ...] '''
    p = OptionParser(usage=usage)
    p.add_option('-u', '--user-agent',
                 action='store',
                 dest='ua',
                 metavar='ua',
                 type='str',
                 help='set the user agent to trick server',
                 default=headers['User-Agent']
                 )
    p.add_option('-p', '--plain',
                 action='store_true',
                 dest='is_plain',
                 metavar='is_plain',
                 help='use plain output format',
                 )
    opt, arg = p.parse_args()
    headers['User-Agent'] = opt.ua
    if len(arg) < 1:
        p.error('<query> must be supplied')
    # query
    for iq, query in enumerate(arg):
        if iq > 0:
            if not opt.is_plain:
                print(chr(0x2500)*os.get_terminal_size().columns)
        paserS(query)
    return

    if len(argv) == 2:
        paserS(argv[1])
    else:
        url = "http://m.dict.cn/"
        for each in range(1,len(argv)):
            url=url+argv[each]+'%20'
        paserM(url)
if __name__ == '__main__':
    main()


