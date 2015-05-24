#!/usr/bin/env python
#coding=utf8


import gevent.monkey
gevent.monkey.patch_all()
import gevent
import gevent.queue

import optparse
import os
import urllib
import urllib2


task_queue = gevent.queue.JoinableQueue(1000)
data_queue = gevent.queue.JoinableQueue(1000)


def crawl_worker():
    while True:
        ident, url = task_queue.get()
        if ident is None:
            task_queue.task_done()
            break

        try:
            text = urllib2.urlopen(url).read()
            data_queue.put((ident,text))
        except Exception as e:
            pass
        task_queue.task_done()


def crawl_dumper(outpath):
    while True:
        ident, text = data_queue.get()
        if ident is None:
            data_queue.task_done()
            break

        filename = os.path.join(outpath, '%s.html' % ident)
        with open(filename, 'wb') as f:
            f.write(text)
        data_queue.task_done()


def crawl_tasker(urlfile, num_workers):
    with open(urlfile) as f:
        for ident, line in enumerate(f):
            url = line.strip()
            task_queue.put((ident,url))

    for i in xrange(num_workers):
        task_queue.put((None,None))


def main():
    optparser = optparse.OptionParser()
    optparser.add_option('-f', '--urlfile', dest='urlfile')
    optparser.add_option('-o', '--outpath', dest='outpath')
    optparser.add_option('-n', '--num_workers', dest='num_workers',
                         type='int', default=3)
    options, args = optparser.parse_args()
    if not options.outpath or not options.urlfile:
        optparser.print_help()
        return

    if not os.path.isdir(options.outpath):
        os.makedirs(options.outpath)

    workers = []
    for i in xrange(options.num_workers):
        workers.append(gevent.spawn(crawl_worker))

    tasker = gevent.spawn(crawl_tasker, options.urlfile, options.num_workers)
    dumper = gevent.spawn(crawl_dumper, options.outpath)

    gevent.joinall([tasker,])
    gevent.joinall(workers)
    task_queue.join()
    data_queue.join()


if __name__ == '__main__':
    import time
    t_start = time.time()
    main()
    t_end = time.time()
    print 'Cost: %s' % (t_end - t_start)
