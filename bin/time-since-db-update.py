#!/usr/bin/env python

import sys
from time import time

import requests


def main(args):
    if args:
        domain = args[0]
    else:
        domain = 'www.mozilla.org'

    url = 'https://{}/bedrock_db_info.json'.format(domain)
    resp = requests.get(url)
    data = resp.json()
    seconds_since = time() - data['updated']
    print 'Database on {} last updated {} minutes ago'.format(domain, int(seconds_since / 60))


if __name__ == '__main__':
    main(sys.argv[1:])
