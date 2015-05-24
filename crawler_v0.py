#!/usr/bin/env python
#coding=utf8


import os
import optparse
import urllib2


def main():
    optparser = optparse.OptionParser()
    optparser.add_option('-f', '--urlfile', dest='urlfile')
    optparser.add_option('-o', '--outpath', dest='outpath')
    options, args = optparser.parse_args()
    if not options.outpath or not options.urlfile:
        optparser.print_help()
        return

    if not os.path.isdir(options.outpath):
        os.makedirs(options.outpath)

    with open(options.urlfile) as f:
        for ident, line in enumerate(f):
            url = line.strip()
            try:
                text = urllib2.urlopen(url).read()
            except Exception as e:
                continue

            filename = os.path.join(options.outpath, '%s.html' % ident)
            with open(filename, 'w') as outf:
                outf.write(text)


if __name__ == '__main__':
    import time
    t_start = time.time()
    main()
    t_end = time.time()
    print 'Cost: %s' % (t_end - t_start)

