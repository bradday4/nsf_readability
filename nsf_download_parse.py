# -*- coding: utf-8 -*-
"""Download all NSF awards from 1959 - 2019"""
#import os
from time import time

import requests


#from multiprocessing.pool import ThreadPool

from clint.textui import progress


def url_response(url):
    """Download file from URL"""
    path, url = url

    r = requests.get(url, stream=True)

    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for ch in progress.bar(r.iter_content(chunk_size=2391975),
                               expected_size=(total_length/1024) + 1):
            if ch:
                f.write(ch)


# %%
# generate urls
X = range(1959, 1961)  # range of dates in nsf database
URL = """https://www.nsf.gov/awardsearch/
download?DownloadFileName={}&All=true"""
URLS = []
j = 1
for i in X:
    #urls.append(("Event{}".format(str(j)), url.format(str(i))))
    URLS.append(URL.format(str(i)))
    j = j+1
# %%
START = time()
for u in URLS:

    url_response(u)

print(f"Time to download: {time() - START}")
#ThreadPool(9).imap_unordered(url_response, urls)
