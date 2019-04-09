#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2019-04-09
@author: Shell.Xu
@copyright: 2019, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
from __future__ import absolute_import, division,\
    print_function, unicode_literals
import sys
import gzip
import base64
import getopt
import binascii


def base64mac(mac):
    return base64.b64encode(binascii.a2b_hex(mac[:6])).decode('latin')+mac[6:]


def compress():
    import re
    re_entry = re.compile('{(?P<mac>.*)}{(?P<name>.*)}')
    rslt = {}
    for line in sys.stdin:
        m = re_entry.match(line.strip())
        if not m:
            raise Exception()
        mac, name = m.groups()
        name = name.strip('." \t')
        rslt.setdefault(name, []).append(base64mac(mac))
    for name, macs in sorted(rslt.items(), key=lambda x: x[0]):
        print('|'.join([name,]+macs))


def lookup(mac, db='ouis.gz'):
    bmac = base64mac(mac.upper().replace(':', '').replace('-', ''))
    with gzip.open(db, mode='rt', encoding='latin') as fi:
        for line in fi:
            name, *macs = line.strip().split('|')
            for m in macs:
                if bmac.startswith(m):
                    return name
    return 'not found'


def main():
    optlist, args = getopt.getopt(sys.argv[1:], 'ch')
    optdict = dict(optlist)
    if '-h' in optdict:
        print(main.__doc__)
        return
    if '-c' in optdict:
        return compress()
    for m in args:
        print(lookup(m))


if __name__ == '__main__':
    main()
