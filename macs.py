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
from os import path


OUI_PATH = path.join(
    path.dirname(path.abspath(__file__)),
    'ouis.gz')


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


def lookup(mac):
    bmac = base64mac(mac.upper().replace(':', '').replace('-', ''))
    with gzip.open(OUI_PATH, mode='rt', encoding='utf-8') as fi:
        for line in fi:
            name, *macs = line.strip().split('|')
            for m in macs:
                if bmac.startswith(m):
                    return name
    return 'not found'


class MacIndex(object):

    def __init__(self):
        self.idx = {}
        with gzip.open(OUI_PATH, mode='rt', encoding='utf-8') as fi:
            for line in fi:
                name, *macs = line.strip().split('|')
                for m in macs:
                    self.idx.setdefault(m[:4], []).append((name, m[4:]))

    def __getitem__(self, mac):
        bmac = base64mac(mac.upper().replace(':', '').replace('-', ''))
        idx, bmac = bmac[:4], bmac[4:]
        l = self.idx.get(idx)
        if not l:
            return 'not found'
        for name, off in l:
            if bmac.startswith(off):
                return name


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
