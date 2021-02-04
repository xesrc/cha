#! /usr/bin/env python3

from sys import argv, stdout, stderr
from urllib import request
from lxml import etree
from optparse import OptionParser

headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}

def paserS(argv):
    url = "http://m.dict.cn/" + request.quote(argv)
    result = ''
    req = request.Request(url, headers=headers)
    page = request.urlopen(req, timeout=10).read()
    page = page.decode("utf-8")
    page = etree.HTML(page)
    words = page.xpath('//*[@id="sctlist"]/li[1]/div[1]/div/div/ul')
    meaning = page.xpath('//*[@id="sctlist"]/li[1]/div[1]/div/div/ul/li/strong')
    if len(meaning)>=1:
        result += (meaning[0].text + '\n')
        phonetic = page.xpath('/html/body/div[1]/div/div[3]/span[1]/bdo')
        if len(phonetic)>=1:
            result += ('en: ' + phonetic[0].text + '\n')
        phonetic = page.xpath('/html/body/div[1]/div/div[3]/span[2]/bdo')
        if len(phonetic)>=1:
            result += ('us: ' + phonetic[0].text + '\n')
    else:
        if len(words)>=1:
            result += ("possible words are :\n")
            result += ("====================\n")
            for line in words[0]:
                result += (line[0].text + '\n')
            result += ("====================\n")
    return result
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
    p.add_option('-s', '--serial',
                 action='store_true',
                 dest='is_serial',
                 metavar='is_serial',
                 help='serially quering (slower), not simultaneously',
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
    if opt.is_serial:
        for iq, query in enumerate(arg):
            if iq > 0:
                if not opt.is_plain:
                    print(chr(0x2500)*os.get_terminal_size().columns)
            try:
                stdout.write(paserS(query))
            except Exception as e:
                stderr.write('%s\n' % e)
    else: # concurrancy
        from concurrent import futures
        outputs = [None] * len(arg)
        with futures.ThreadPoolExecutor(max_workers=len(arg)) as e:
            results = dict(
                    (e.submit(paserS, query), iq)
                    for iq, query in enumerate(arg)
                    )
            for future in futures.as_completed(results.keys()):
                iq = results[future]
                try:
                    outputs[iq] = (True, future.result())
                except Exception as e:
                    outputs[iq] = (False, 'failed to parse {}\n{}\n'.format(arg[iq], e))
        for iout, output in enumerate(outputs):
            if iout > 0:
                if not opt.is_plain:
                    print(chr(0x2500)*os.get_terminal_size().columns)
            if output[0]:
                stdout.write(output[1])
            else:
                stderr.write(output[1])
    # end if opt.is_serial
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


